import os
import numpy as np
from rope_train.copy_paste import paste_patch, augment

def test_paste_changes_image_keeps_shape():
    bg = np.full((128, 128, 3), 50, np.uint8)
    patch = np.full((20, 20, 3), 255, np.uint8)
    out = paste_patch(bg, patch, seed=1)
    assert out.shape == bg.shape
    assert not np.array_equal(out, bg)

def test_augment_writes_files(tmp_path):
    import cv2
    nd = tmp_path / "normal"; pd = tmp_path / "patches"; od = tmp_path / "out"
    nd.mkdir(); pd.mkdir()
    cv2.imwrite(str(nd / "bg.jpg"), np.full((128, 128, 3), 50, np.uint8))
    cv2.imwrite(str(pd / "p.png"), np.full((20, 20, 3), 255, np.uint8))
    n = augment(str(pd), str(nd), str(od), count=5)
    assert n == 5
    assert len(os.listdir(od)) == 5
