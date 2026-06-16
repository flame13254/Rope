from rope_edge.smoothing import SlidingWindow

def test_window_outputs_fault_when_ratio_met():
    w = SlidingWindow(window_sec=1.5, ratio=0.8, conf_thresh=0.5)
    # 5 帧全部达标 -> 1
    for t in range(5):
        out = w.update(status=1, conf=0.9, now=t * 0.1)
    assert out == 1

def test_window_outputs_normal_when_below_ratio():
    w = SlidingWindow(window_sec=1.5, ratio=0.8, conf_thresh=0.5)
    # 交替: 达标占比 0.5 < 0.8 -> 0
    out = 0
    for i in range(6):
        out = w.update(status=i % 2, conf=0.9, now=i * 0.1)
    assert out == 0

def test_low_confidence_not_counted():
    w = SlidingWindow(window_sec=1.5, ratio=0.8, conf_thresh=0.5)
    out = 0
    for t in range(5):
        out = w.update(status=1, conf=0.3, now=t * 0.1)  # 置信度不达标
    assert out == 0

def test_old_frames_expire():
    w = SlidingWindow(window_sec=1.0, ratio=0.8, conf_thresh=0.5)
    w.update(status=0, conf=0.9, now=0.0)
    # 2 秒后旧帧过期, 新窗口只剩达标帧
    out = 0
    for t in range(5):
        out = w.update(status=1, conf=0.9, now=2.0 + t * 0.1)
    assert out == 1
