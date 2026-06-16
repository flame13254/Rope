import time
import numpy as np
import cv2


def _normal(sz=256):
    img = np.full((sz, sz, 3), 40, np.uint8)
    for y in range(-sz, sz, 12):
        cv2.line(img, (0, y), (sz, y + sz), (200, 200, 200), 3)
    return img


def _fault(sz=256):
    img = _normal(sz)
    for y in range(-sz, sz, 30):
        cv2.line(img, (0, y + sz), (sz, y), (230, 230, 230), 3)
    return img


class SyntheticSource:
    def __init__(self, fps=25, count=None):
        self.fps = fps
        self.count = count

    def frames(self):
        i = 0
        while self.count is None or i < self.count:
            yield _normal() if i % 2 == 0 else _fault()
            i += 1


class FileSource:
    def __init__(self, path, fps=25):
        self.path = path
        self.fps = fps

    def frames(self):
        cap = cv2.VideoCapture(self.path)
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                yield frame
        finally:
            cap.release()


class RtspSource:
    def __init__(self, url, fps=25, max_retries=5):
        self.url = url
        self.fps = fps
        self.max_retries = max_retries

    def frames(self):
        retries = 0
        while retries <= self.max_retries:
            cap = cv2.VideoCapture(self.url)
            if not cap.isOpened():
                retries += 1
                print(f"[warn] RTSP 打开失败, 重试 {retries}/{self.max_retries}")
                time.sleep(min(2 ** retries, 30))
                continue
            retries = 0
            while True:
                ok, frame = cap.read()
                if not ok:
                    print("[warn] RTSP 断流, 重连")
                    break
                yield frame
            cap.release()
            retries += 1


def make_source(cfg):
    t = cfg["type"]
    if t == "synthetic":
        return SyntheticSource(fps=cfg.get("fps", 25))
    if t == "file":
        return FileSource(cfg["path"], fps=cfg.get("fps", 25))
    if t == "rtsp":
        return RtspSource(cfg["path"], fps=cfg.get("fps", 25))
    raise ValueError(f"未知 source 类型: {t}")
