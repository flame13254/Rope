from rope_edge.source import SyntheticSource, FileSource, RtspSource, make_source

def test_synthetic_source_yields_frames():
    src = SyntheticSource(fps=25, count=4)
    frames = list(src.frames())
    assert len(frames) == 4
    assert frames[0].shape == (256, 256, 3)

def test_make_source_types():
    assert isinstance(make_source({"type": "synthetic", "path": "", "fps": 25}), SyntheticSource)
    assert isinstance(make_source({"type": "file", "path": "x.mp4", "fps": 25}), FileSource)
    assert isinstance(make_source({"type": "rtsp", "path": "rtsp://x", "fps": 25}), RtspSource)
