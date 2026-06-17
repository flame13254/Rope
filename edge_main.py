"""边缘 AI 推理主进程入口。"""
import argparse
from rope_edge.config import load_edge_config
from rope_edge.source import make_source
from rope_edge.roi import make_roi
from rope_edge.classifier import make_classifier
from rope_edge.smoothing import SlidingWindow
from rope_edge.publisher import make_publisher
from rope_edge.pipeline import Pipeline


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/edge.yaml")
    ap.add_argument("--max-frames", type=int, default=None, help="冒烟/测试限步")
    a = ap.parse_args()
    cfg = load_edge_config(a.config)
    sm = cfg["smoothing"]
    pipeline = Pipeline(
        source=make_source(cfg["source"]),
        roi=make_roi(cfg["roi"]),
        classifier=make_classifier(cfg["model"]),
        smoothing=SlidingWindow(sm["window_sec"], sm["ratio"], sm["conf_thresh"]),
        publisher=make_publisher(cfg),
        camera_id=cfg["camera_id"],
        frame_stride=cfg["frame_stride"],
        publish_interval_sec=cfg["publish_interval_sec"],
    )
    pipeline.run(max_frames=a.max_frames)


if __name__ == "__main__":
    main()
