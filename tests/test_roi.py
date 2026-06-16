import numpy as np
from rope_edge.roi import FixedROI, make_roi

def test_fixed_roi_crops_region():
    frame = np.zeros((720, 1280, 3), np.uint8)
    roi = FixedROI(x=100, y=50, w=200, h=150)
    out = roi.crop(frame)
    assert out.shape == (150, 200, 3)

def test_fixed_roi_clamps_out_of_bounds():
    frame = np.zeros((100, 100, 3), np.uint8)
    roi = FixedROI(x=80, y=80, w=200, h=200)  # 越界
    out = roi.crop(frame)
    assert out.shape[0] == 20 and out.shape[1] == 20  # 夹取到画面内

def test_make_roi_factory():
    roi = make_roi({"type": "fixed", "x": 0, "y": 0, "w": 10, "h": 10})
    assert isinstance(roi, FixedROI)
