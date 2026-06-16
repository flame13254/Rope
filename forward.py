"""FFmpeg 子码流 -c:v copy 推 RTMP (免编码, 去音频)。"""
import argparse
import subprocess
import time
from rope_edge.config import load_edge_config


def build_ffmpeg_cmd(sub_url, rtmp_url):
    return ["ffmpeg", "-rtsp_transport", "tcp", "-i", sub_url,
            "-c:v", "copy", "-an", "-f", "flv", rtmp_url]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/edge.yaml")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令")
    a = ap.parse_args()
    fwd = load_edge_config(a.config)["forward"]
    cmd = build_ffmpeg_cmd(fwd["sub_url"], fwd["rtmp_url"])
    if a.dry_run:
        print(" ".join(cmd))
        return
    while True:  # 简单守护: 退出即重启
        print("[forward] 启动:", " ".join(cmd))
        subprocess.run(cmd)
        print("[forward] ffmpeg 退出, 2s 后重启")
        time.sleep(2)


if __name__ == "__main__":
    main()
