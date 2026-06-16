import os
import glob
import numpy as np
import cv2


def paste_patch(bg, patch, seed=None, max_scale=1.2, min_scale=0.8, max_angle=15):
    """把故障小块随机贴到背景。禁用大角度旋转(|angle|<=max_angle)。"""
    rng = np.random.default_rng(seed)
    s = rng.uniform(min_scale, max_scale)
    ph, pw = patch.shape[:2]
    nw, nh = max(1, int(pw * s)), max(1, int(ph * s))
    p = cv2.resize(patch, (nw, nh))
    angle = rng.uniform(-max_angle, max_angle)
    M = cv2.getRotationMatrix2D((nw / 2, nh / 2), angle, 1.0)
    p = cv2.warpAffine(p, M, (nw, nh), borderMode=cv2.BORDER_REFLECT)
    H, W = bg.shape[:2]
    if nw >= W or nh >= H:
        p = cv2.resize(p, (W // 4, H // 4))
        nh, nw = p.shape[:2]
    x = int(rng.integers(0, W - nw))
    y = int(rng.integers(0, H - nh))
    out = bg.copy()
    out[y:y + nh, x:x + nw] = p
    return out


def augment(patches_dir, normal_dir, out_dir, count=50, seed=0):
    os.makedirs(out_dir, exist_ok=True)
    patches = [cv2.imread(p) for p in glob.glob(os.path.join(patches_dir, "*"))]
    bgs = [cv2.imread(p) for p in glob.glob(os.path.join(normal_dir, "*"))]
    patches = [x for x in patches if x is not None]
    bgs = [x for x in bgs if x is not None]
    if not patches or not bgs:
        raise ValueError("patches 或 normal 背景为空")
    rng = np.random.default_rng(seed)
    for i in range(count):
        bg = bgs[rng.integers(len(bgs))]
        patch = patches[rng.integers(len(patches))]
        out = paste_patch(bg, patch, seed=int(rng.integers(1 << 30)))
        cv2.imwrite(os.path.join(out_dir, f"cp{i:04d}.jpg"), out)
    return count
