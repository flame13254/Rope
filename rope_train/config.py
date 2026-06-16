import yaml


def load_experiments(path):
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    common = cfg.get("common", {})
    runs = []
    for m in cfg["models"]:
        merged = {**common, **m}
        for key in ("name", "weights", "imgsz", "epochs", "data"):
            if key not in merged:
                raise ValueError(f"run {m.get('name', '?')} 缺少字段: {key}")
        runs.append(merged)
    return runs


def resolve_device(device):
    if device != "auto":
        return device
    try:
        import torch
        return "0" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"
