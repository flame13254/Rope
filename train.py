"""配置驱动的分类训练: 遍历 experiments.yaml 训练每个 run。"""
import argparse
from ultralytics import YOLO
from rope_train.config import load_experiments, resolve_device

# 抗环境光的在线增强 + 禁用大角度旋转(方案第八节)
AUG = dict(hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, degrees=0.0,
           translate=0.1, scale=0.5, fliplr=0.5, erasing=0.4)


def train_run(run, epochs_override=None):
    device = resolve_device(run["device"])
    model = YOLO(run["weights"])
    model.train(
        task="classify",
        data=run["data"],
        epochs=epochs_override or run["epochs"],
        imgsz=run["imgsz"],
        batch=run["batch"],
        device=device,
        project=run["project"],
        name=run["name"],
        exist_ok=True,
        **AUG,
    )
    print(f"[done] {run['name']} -> {run['project']}/{run['name']}/weights/best.pt")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments.yaml")
    ap.add_argument("--only", help="只训练指定 run 名(冒烟用)")
    ap.add_argument("--smoke-epochs", type=int, help="覆盖 epochs(冒烟用)")
    a = ap.parse_args()
    runs = load_experiments(a.config)
    if a.only:
        runs = [r for r in runs if r["name"] == a.only]
    for r in runs:
        train_run(r, a.smoke_epochs)


if __name__ == "__main__":
    main()
