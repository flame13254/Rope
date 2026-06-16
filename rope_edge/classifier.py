class MockClassifier:
    """无需模型, 供骨架验证。mode: alternate|normal|fault"""

    def __init__(self, mode="alternate"):
        self.mode = mode
        self.i = -1

    def predict(self, roi):
        self.i += 1
        if self.mode == "normal":
            return (0, 0.1)
        if self.mode == "fault":
            return (1, 0.9)
        return (self.i % 2, 0.9)  # alternate


class YoloClassifier:
    """YOLO 加载 pt/onnx/engine/openvino 任意后端格式。"""

    def __init__(self, model_path, device="auto"):
        from ultralytics import YOLO  # 惰性导入
        from rope_train.config import resolve_device
        self.model = YOLO(model_path)
        self.device = resolve_device(device)

    def predict(self, roi):
        r = self.model.predict(roi, device=self.device, verbose=False)[0]
        top1 = int(r.probs.top1)
        conf = float(r.probs.top1conf)
        name = r.names[top1]
        status = 1 if name == "fault" else 0
        return (status, conf)


def make_classifier(cfg):
    if cfg["type"] == "mock":
        return MockClassifier(mode=cfg.get("mode", "alternate"))
    if cfg["type"] == "yolo":
        return YoloClassifier(cfg["path"], cfg.get("device", "auto"))
    raise ValueError(f"未知 model 类型: {cfg['type']}")
