from datetime import datetime, timezone, timedelta
from rope_edge.publisher import build_payload, LogPublisher, make_publisher

def test_payload_fields_and_timezone():
    now = datetime(2026, 6, 16, 15, 20, 0, tzinfo=timezone(timedelta(hours=8)))
    p = build_payload("PTZ_01", status=1, confidence=0.923456, now=now)
    assert p["timestamp"] == "2026-06-16T15:20:00+08:00"
    assert p["camera_id"] == "PTZ_01"
    assert p["status"] == 1
    assert p["ai_confidence"] == 0.9235
    assert "fault_boxes" not in p

def test_make_publisher_log_when_disabled():
    cfg = {"mqtt": {"enabled": False, "host": "x", "port": 1883,
                    "topic": "t", "qos": 1}}
    pub = make_publisher(cfg)
    assert isinstance(pub, LogPublisher)
