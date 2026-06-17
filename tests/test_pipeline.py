from datetime import datetime, timezone, timedelta
from rope_edge.pipeline import Pipeline

class _Src:
    def __init__(self, n): self.n = n
    def frames(self):
        for i in range(self.n):
            yield ("frame", i)

class _ROI:
    def crop(self, f): return f

class _Clf:
    def __init__(self, calls): self.calls = calls
    def predict(self, roi):
        self.calls.append(roi)
        return (1, 0.9)

class _Smooth:
    def update(self, status, conf, now): return status

class _Pub:
    def __init__(self, out): self.out = out
    def publish(self, payload): self.out.append(payload)

def _now_fn():
    base = datetime(2026, 6, 16, 15, 20, 0, tzinfo=timezone(timedelta(hours=8)))
    t = {"v": base}
    def f():
        cur = t["v"]; t["v"] = cur + timedelta(seconds=1); return cur
    return f

def test_pipeline_stride_and_publish_on_change():
    calls, pubs = [], []
    # publish_interval_sec=100 大于测试时长 -> 仅状态变化驱动发布
    p = Pipeline(_Src(9), _ROI(), _Clf(calls), _Smooth(), _Pub(pubs),
                 camera_id="C1", frame_stride=3, publish_interval_sec=100, now_fn=_now_fn())
    p.run()
    assert len(calls) == 3          # 9 帧 stride 3 -> idx 0,3,6
    assert len(pubs) == 1           # status 恒为 1, 仅首帧发布
    assert pubs[0]["status"] == 1 and pubs[0]["camera_id"] == "C1"

def test_pipeline_periodic_resend():
    calls, pubs = [], []
    # publish_interval_sec=0 -> 每个检测周期都重发当前状态(电平式)
    p = Pipeline(_Src(9), _ROI(), _Clf(calls), _Smooth(), _Pub(pubs),
                 camera_id="C1", frame_stride=3, publish_interval_sec=0, now_fn=_now_fn())
    p.run()
    assert len(pubs) == 3           # idx 0,3,6 每次都重发

def test_pipeline_max_frames():
    calls, pubs = [], []
    p = Pipeline(_Src(100), _ROI(), _Clf(calls), _Smooth(), _Pub(pubs),
                 camera_id="C1", frame_stride=1, publish_interval_sec=100, now_fn=_now_fn())
    p.run(max_frames=5)
    assert len(calls) == 5
