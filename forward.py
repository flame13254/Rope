"""FFmpeg 子码流 -c:v copy 推 RTMP (免编码, 去音频)。

设计目标: 网络波动/MediaMTX 重启时, ffmpeg 尽快退出, 守护循环按退避重连。
注: ffmpeg 的 -reconnect 仅对 HTTP 输入有效, RTSP/RTMP 必须靠外部守护。
"""
import argparse
import subprocess
import time
from rope_edge.config import load_edge_config


def build_ffmpeg_cmd(sub_url, rtmp_url,
                     rtsp_timeout_us=5000000,
                     extra_input_args=None,
                     extra_output_args=None):
    """构造 ffmpeg 命令。

    - rtsp_timeout_us: RTSP socket I/O 超时(微秒)。卡死时尽快退出供守护重连。
      ⚠️ 现场如果是 ffmpeg ≥5 的部分构建, 参数名可能改为 -timeout, 此时把
         extra_input_args 配置成 ["-timeout", "5000000"] 并把本参数置 0 跳过。
    - extra_input_args/extra_output_args: 现场可在 edge.yaml 调试附加 flag,
      不需要改代码(例如 -fflags nobuffer 等)。
    """
    cmd = ["ffmpeg", "-rtsp_transport", "tcp"]
    if rtsp_timeout_us and rtsp_timeout_us > 0:
        cmd += ["-stimeout", str(int(rtsp_timeout_us))]
    if extra_input_args:
        cmd += list(extra_input_args)
    cmd += ["-i", sub_url, "-c:v", "copy", "-an"]
    if extra_output_args:
        cmd += list(extra_output_args)
    cmd += ["-f", "flv", rtmp_url]
    return cmd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/edge.yaml")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令")
    a = ap.parse_args()
    fwd = load_edge_config(a.config)["forward"]
    cmd = build_ffmpeg_cmd(
        fwd["sub_url"], fwd["rtmp_url"],
        rtsp_timeout_us=fwd.get("rtsp_timeout_us", 5000000),
        extra_input_args=fwd.get("extra_input_args"),
        extra_output_args=fwd.get("extra_output_args"),
    )
    if a.dry_run:
        print(" ".join(cmd))
        return
    # 指数退避重连: 初值->上限, 避免 MediaMTX 未起来时疯狂重连
    lo, hi = fwd.get("reconnect_backoff", [2, 10])
    delay = lo
    while True:
        print("[forward] 启动:", " ".join(cmd))
        t0 = time.monotonic()
        try:
            subprocess.run(cmd)
        except FileNotFoundError:
            print("[forward] 系统未找到 ffmpeg, 请安装并加入 PATH")
            return
        elapsed = time.monotonic() - t0
        if elapsed >= 30:   # 跑过一段时间再断: 视为长稳后偶发故障, 退避复位
            delay = lo
        print(f"[forward] ffmpeg 退出(运行 {elapsed:.1f}s), {delay}s 后重启")
        time.sleep(delay)
        if elapsed < 30:
            delay = min(hi, delay * 2)


if __name__ == "__main__":
    main()
