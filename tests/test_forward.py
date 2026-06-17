from forward import build_ffmpeg_cmd


def test_build_ffmpeg_cmd_basic():
    cmd = build_ffmpeg_cmd("rtsp://cam/sub", "rtmp://cloud/live/spooling")
    assert cmd[0] == "ffmpeg"
    # 免编码 + 去音频
    assert "-c:v" in cmd and cmd[cmd.index("-c:v") + 1] == "copy"
    assert "-an" in cmd
    assert cmd[cmd.index("-i") + 1] == "rtsp://cam/sub"
    assert cmd[-1] == "rtmp://cloud/live/spooling"
    assert cmd[cmd.index("-f") + 1] == "flv"
    # RTSP I/O 超时(默认), 卡死时尽快退出供守护重连
    assert "-stimeout" in cmd
    assert cmd[cmd.index("-stimeout") + 1] == "5000000"


def test_build_ffmpeg_cmd_extra_args_and_no_timeout():
    cmd = build_ffmpeg_cmd(
        "rtsp://cam/sub", "rtmp://cloud/live/spooling",
        rtsp_timeout_us=0,
        extra_input_args=["-fflags", "nobuffer"],
        extra_output_args=["-flvflags", "no_duration_filesize"],
    )
    assert "-stimeout" not in cmd
    # 输入侧 extra 在 -i 之前
    assert cmd.index("-fflags") < cmd.index("-i")
    # 输出侧 extra 在 -f flv 之前
    assert cmd.index("-flvflags") < cmd.index("-f")
    assert cmd[cmd.index("-flvflags") + 1] == "no_duration_filesize"


def test_build_ffmpeg_cmd_rtsp_transport_tcp():
    cmd = build_ffmpeg_cmd("rtsp://cam/sub", "rtmp://cloud/live/spooling")
    assert cmd[cmd.index("-rtsp_transport") + 1] == "tcp"
