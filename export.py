"""把每个 run 的 best.pt 导出为可用后端格式。"""
import argparse
import os
from ultralytics import YOLO
from rope_train.config import load_experiments, resolve_device, find_best
from rope_train.backends import export_targets


def export_run(run):
    best = find_best(run)
    if not os.path.exists(best):
        print(f"[skip] 未找到 {best}, 先训练")
        return
    has_cuda = resolve_device("auto") != "cpu"
    model = YOLO(best)
    for fmt in export_targets(has_cuda):
        try:
            kw = dict(format=fmt, imgsz=run["imgsz"])
            if fmt == "engine":
                kw.update(half=True, device=0)
            model.export(**kw)
            print(f"[ok] {run['name']} -> {fmt}")
        except Exception as e:
            print(f"[warn] {run['name']} 导出 {fmt} 失败: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments.yaml")
    ap.add_argument("--only")
    a = ap.parse_args()
    runs = load_experiments(a.config)
    if a.only:
        runs = [r for r in runs if r["name"] == a.only]
    for r in runs:
        export_run(r)


if __name__ == "__main__":
    main()
