"""对每个 run 实测 fault 类 F1 / 单帧 ms / 内存 MB, 输出对比表。"""
import argparse
import glob
import os
import time
import numpy as np
from ultralytics import YOLO
from rope_train.config import load_experiments, resolve_device, find_best


def f1_score(tp, fp, fn):
    if tp == 0:
        return 0.0
    prec = tp / (tp + fp)
    rec = tp / (tp + fn)
    return 2 * prec * rec / (prec + rec)


def _eval(model, val_dir, imgsz, device):
    """对 val/{normal,fault} 预测, 以 'fault' 为正类统计混淆。"""
    tp = fp = fn = 0
    times = []
    for cls in ("normal", "fault"):
        for img in glob.glob(os.path.join(val_dir, cls, "*")):
            t0 = time.perf_counter()
            r = model.predict(img, imgsz=imgsz, device=device, verbose=False)[0]
            times.append((time.perf_counter() - t0) * 1000)
            pred = r.names[int(r.probs.top1)]
            if cls == "fault" and pred == "fault":
                tp += 1
            elif cls == "normal" and pred == "fault":
                fp += 1
            elif cls == "fault" and pred != "fault":
                fn += 1
    return f1_score(tp, fp, fn), float(np.mean(times)) if times else 0.0


def _mem_mb(device):
    if device != "cpu":
        try:
            import torch
            return torch.cuda.max_memory_allocated() / 1024 / 1024
        except Exception:
            return 0.0
    try:
        import psutil
        return psutil.Process().memory_info().rss / 1024 / 1024
    except Exception:
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments.yaml")
    ap.add_argument("--val", default="dataset_cls/val")
    a = ap.parse_args()
    device = resolve_device("auto")
    rows = []
    for run in load_experiments(a.config):
        best = find_best(run)
        if not os.path.exists(best):
            continue
        model = YOLO(best)
        f1, ms = _eval(model, a.val, run["imgsz"], device)
        rows.append((run["name"], f1, ms, _mem_mb(device)))
    lines = ["| run | F1(fault) | 单帧ms | 内存MB |", "|---|---|---|---|"]
    csv = ["run,f1,ms,mem_mb"]
    for n, f1, ms, mem in rows:
        lines.append(f"| {n} | {f1:.3f} | {ms:.1f} | {mem:.0f} |")
        csv.append(f"{n},{f1:.4f},{ms:.2f},{mem:.1f}")
    os.makedirs("runs", exist_ok=True)
    open("runs/benchmark.md", "w", encoding="utf-8").write("\n".join(lines))
    open("runs/benchmark.csv", "w", encoding="utf-8").write("\n".join(csv))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
