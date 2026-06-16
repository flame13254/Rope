import yaml

REQUIRED = ("camera_id", "source", "frame_stride", "roi", "model",
            "smoothing", "mqtt", "forward", "heartbeat_sec")


def load_edge_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for k in REQUIRED:
        if k not in cfg:
            raise ValueError(f"edge 配置缺少字段: {k}")
    return cfg
