from rope_edge.config import load_edge_config

def test_load_edge_config_required_keys():
    cfg = load_edge_config("configs/edge.yaml")
    for k in ("camera_id", "source", "frame_stride", "roi", "model",
              "smoothing", "mqtt", "forward", "heartbeat_sec"):
        assert k in cfg
    assert cfg["frame_stride"] == 3
    assert cfg["source"]["type"] == "synthetic"

def test_load_edge_config_missing_key(tmp_path):
    import pytest
    p = tmp_path / "bad.yaml"
    p.write_text("camera_id: X\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_edge_config(str(p))
