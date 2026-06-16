from forward import build_ffmpeg_cmd

def test_build_ffmpeg_cmd():
    cmd = build_ffmpeg_cmd("rtsp://cam/sub", "rtmp://cloud/live/spooling")
    assert cmd[0] == "ffmpeg"
    # 免编码 + 去音频
    assert "-c:v" in cmd and cmd[cmd.index("-c:v") + 1] == "copy"
    assert "-an" in cmd
    assert cmd[cmd.index("-i") + 1] == "rtsp://cam/sub"
    assert cmd[-1] == "rtmp://cloud/live/spooling"
    assert cmd[cmd.index("-f") + 1] == "flv"
