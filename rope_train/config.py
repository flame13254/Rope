import glob
import os
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


def find_best(run):
    """定位某个 run 的 best.pt。Ultralytics 分类模式会插入 classify/ 子目录,
    标准路径找不到时在 project 下递归查找 <name>/weights/best.pt。"""
    cand = os.path.join(run["project"], run["name"], "weights", "best.pt")
    if os.path.exists(cand):
        return cand
    hits = glob.glob(
        os.path.join(run["project"], "**", run["name"], "weights", "best.pt"),
        recursive=True,
    )
    return hits[0] if hits else cand
