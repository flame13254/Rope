import json
from datetime import datetime


def build_payload(camera_id, status, confidence, now=None):
    if now is None:
        now = datetime.now().astimezone()
    return {
        "timestamp": now.isoformat(),
        "camera_id": camera_id,
        "status": int(status),
        "ai_confidence": round(float(confidence), 4),
    }


class LogPublisher:
    """MQTT 关闭/dry-run 时打印 JSON。"""

    def publish(self, payload):
        print(json.dumps(payload, ensure_ascii=False))


class MqttPublisher:
    def __init__(self, host, port, topic, qos, lwt_topic=None, device_id=None):
        import paho.mqtt.client as mqtt  # 惰性导入
        self.topic = topic
        self.qos = qos
        self.client = mqtt.Client()
        self._buf = []
        # 遗嘱(LWT): 边缘异常掉线时, broker 自动替它发 offline 通知订阅者
        if lwt_topic:
            offline = json.dumps({"device_id": device_id, "online": False},
                                 ensure_ascii=False)
            self.client.will_set(lwt_topic, offline, qos=1, retain=True)
        try:
            self.client.connect(host, port, keepalive=60)
            self.client.loop_start()
            if lwt_topic:  # 连上后即发 online (retained), 与遗嘱配对
                online = json.dumps({"device_id": device_id, "online": True},
                                    ensure_ascii=False)
                self.client.publish(lwt_topic, online, qos=1, retain=True)
        except Exception as e:
            print(f"[warn] MQTT 连接失败, 暂存待发: {e}")

    def publish(self, payload):
        msg = json.dumps(payload, ensure_ascii=False)
        info = self.client.publish(self.topic, msg, qos=self.qos)
        if info.rc != 0:
            self._buf.append(msg)
            print(f"[warn] MQTT 发布失败(rc={info.rc}), 已缓存")


def make_publisher(cfg):
    m = cfg["mqtt"]
    if m.get("enabled"):
        return MqttPublisher(m["host"], m["port"], m["topic"], m["qos"],
                             lwt_topic=m.get("lwt_topic"),
                             device_id=cfg.get("camera_id"))
    return LogPublisher()
