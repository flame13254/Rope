from datetime import datetime
from rope_edge.publisher import build_payload


class Pipeline:
    def __init__(self, source, roi, classifier, smoothing, publisher,
                 camera_id, frame_stride=3, publish_interval_sec=1.0, now_fn=None):
        self.source = source
        self.roi = roi
        self.classifier = classifier
        self.smoothing = smoothing
        self.publisher = publisher
        self.camera_id = camera_id
        self.frame_stride = max(1, int(frame_stride))
        self.publish_interval_sec = publish_interval_sec
        self.now_fn = now_fn or (lambda: datetime.now().astimezone())

    def run(self, max_frames=None):
        last_status = None
        last_pub_ts = None
        processed = 0
        for idx, frame in enumerate(self.source.frames()):
            if idx % self.frame_stride != 0:
                continue
            roi_img = self.roi.crop(frame)
            status, conf = self.classifier.predict(roi_img)
            now = self.now_fn()
            smoothed = self.smoothing.update(status, conf, now.timestamp())
            changed = smoothed != last_status
            # 状态变化立即发; 否则按 publish_interval_sec 重发当前状态(电平式, 可自愈)
            due = (last_pub_ts is not None
                   and now.timestamp() - last_pub_ts >= self.publish_interval_sec)
            if last_pub_ts is None or changed or due:
                self.publisher.publish(
                    build_payload(self.camera_id, smoothed, conf, now))
                last_status = smoothed
                last_pub_ts = now.timestamp()
            processed += 1
            if max_frames and processed >= max_frames:
                break
