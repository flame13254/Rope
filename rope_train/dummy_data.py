import os
import numpy as np
import cv2


def _parallel(sz=256):
    """正常: 平行斜纹。"""
    img = np.full((sz, sz, 3), 40, np.uint8)
    for y in range(-sz, sz, 12):
        cv2.line(img, (0, y), (sz, y + sz), (200, 200, 200), 3)
    return img


def _crossed(sz=256):
    """故障: 平行纹上叠加交叉线 + 隆起斑块。"""
    img = _parallel(sz)
    for y in range(-sz, sz, 30):
        cv2.line(img, (0, y + sz), (sz, y), (230, 230, 230), 3)
    cv2.circle(img, (sz // 2, sz // 2), sz // 8, (255, 255, 255), -1)
    return img


def _save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, img)


def make_dummy_dataset(root, n_train=20, n_val=6):
    rng = np.random.default_rng(0)
    for split, n in (("train", n_train), ("val", n_val)):
        for i in range(n):
            noise = rng.integers(-15, 15, (256, 256, 3), dtype=np.int16)
            normal = np.clip(_parallel().astype(np.int16) + noise, 0, 255).astype(np.uint8)
            fault = np.clip(_crossed().astype(np.int16) + noise, 0, 255).astype(np.uint8)
            _save(normal, os.path.join(root, split, "normal", f"n{i:03d}.jpg"))
            _save(fault, os.path.join(root, split, "fault", f"f{i:03d}.jpg"))


def make_dummy_patches(out_dir, n=8):
    os.makedirs(out_dir, exist_ok=True)
    for i in range(n):
        p = np.full((48, 48, 3), 30, np.uint8)
        cv2.line(p, (0, 0), (48, 48), (255, 255, 255), 3)
        cv2.line(p, (48, 0), (0, 48), (255, 255, 255), 3)
        cv2.imwrite(os.path.join(out_dir, f"patch{i:02d}.png"), p)
