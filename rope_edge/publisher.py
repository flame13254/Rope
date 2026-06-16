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
    def __init__(self, host, port, topic, qos):
        import paho.mqtt.client as mqtt  # 惰性导入
        self.topic = topic
        self.qos = qos
        self.client = mqtt.Client()
        self._buf = []
        try:
            self.client.connect(host, port, keepalive=60)
            self.client.loop_start()
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
        return MqttPublisher(m["host"], m["port"], m["topic"], m["qos"])
    return LogPublisher()
