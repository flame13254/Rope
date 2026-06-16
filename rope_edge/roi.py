class FixedROI:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = int(x), int(y), int(w), int(h)

    def crop(self, frame):
        H, W = frame.shape[:2]
        x0 = max(0, min(self.x, W))
        y0 = max(0, min(self.y, H))
        x1 = max(x0, min(self.x + self.w, W))
        y1 = max(y0, min(self.y + self.h, H))
        return frame[y0:y1, x0:x1]


def make_roi(cfg):
    if cfg.get("type", "fixed") == "fixed":
        return FixedROI(cfg["x"], cfg["y"], cfg["w"], cfg["h"])
    raise ValueError(f"未知 ROI 类型: {cfg.get('type')}")
