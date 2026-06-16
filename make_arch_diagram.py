# -*- coding: utf-8 -*-
"""生成《智能排绳故障检测与数字孪生系统》总体架构图 (PNG)。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1700, 1320
SCALE = 2  # 2x 超采样后缩小，文字更清晰
img = Image.new("RGB", (W * SCALE, H * SCALE), "white")
d = ImageDraw.Draw(img)

FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size * SCALE)


def s(*vals):
    return tuple(v * SCALE for v in vals)


def rrect(box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(s(*box), radius=radius * SCALE, fill=fill,
                        outline=outline, width=width * SCALE)


def ctext(cx, y, text, font, fill="black", anchor="ma"):
    d.text(s(cx, y), text, font=font, fill=fill, anchor=anchor)


def box(box_xy, title, lines, border, title_color):
    x0, y0, x1, y1 = box_xy
    rrect(box_xy, 12, fill="white", outline=border, width=3)
    cx = (x0 + x1) / 2
    ctext(cx, y0 + 14, title, f(21, True), fill=title_color)
    yy = y0 + 54
    for ln in lines:
        ctext(cx, yy, ln, f(17), fill="#222222")
        yy += 30


def varrow(x, y0, y1, label=None, label_side="right"):
    x_, y0_, y1_ = x * SCALE, y0 * SCALE, y1 * SCALE
    d.line([(x_, y0_), (x_, y1_)], fill="#3A3A3A", width=3 * SCALE)
    ah = 9 * SCALE
    d.polygon([(x_, y1_), (x_ - ah, y1_ - ah), (x_ + ah, y1_ - ah)], fill="#3A3A3A")
    if label:
        ly = (y0 + y1) / 2
        font = f(16)
        tb = d.textbbox(s(x, ly), label, font=font, anchor="mm")
        pad = 6 * SCALE
        bg = [tb[0] - pad, tb[1] - pad // 2, tb[2] + pad, tb[3] + pad // 2]
        d.rounded_rectangle(bg, radius=5 * SCALE, fill="white", outline="#CFCFCF", width=1 * SCALE)
        d.text(s(x, ly), label, font=font, fill="#1A1A1A", anchor="mm")


def band(y0, y1, header, hdr_bg, body_bg):
    rrect((50, y0, 1650, y1), 14, fill=body_bg, outline=hdr_bg, width=2)
    rrect((50, y0, 1650, y0 + 46), 14, fill=hdr_bg)
    d.rectangle(s(50, y0 + 30, 1650, y0 + 46), fill=hdr_bg)
    d.text(s(72, y0 + 9), header, font=f(22, True), fill="white", anchor="la")


# ---- Title ----
ctext(W / 2, 26, "智能排绳故障检测与数字孪生系统  总体架构", f(34, True), fill="#10243B")

LCX, RCX = 470, 1230  # 左右两列中心
# 列宽
LBX = (LCX - 340, RCX + 340)

# ===== ① 感知获取层 =====
band(96, 312, "①  感知获取层 · 现场设备端", "#2E5C8A", "#EAF2FB")
box((850 - 430, 150, 850 + 430, 300), "PTZ 球形摄像头",
    ["编码强制 H.264 · CBR · 1080p+   ·   关闭 3D 降噪（保护螺旋纹理）",
     "CPL 偏振镜  ·  侧向 / 低角度补光  ·  锁定预置位 Preset"],
    "#2E5C8A", "#2E5C8A")

# 分叉箭头到第二层
fy = 330
d.line([s(850, 300)[0], s(850, 300)[1], s(850, fy)[0], s(850, fy)[1]], fill="#3A3A3A", width=3 * SCALE)
d.line([s(LCX, fy)[0], s(LCX, fy)[1], s(RCX, fy)[0], s(RCX, fy)[1]], fill="#3A3A3A", width=3 * SCALE)
varrow(LCX, fy, 392, "主码流 RTSP/H.264 （推理）")
varrow(RCX, fy, 392, "子码流 RTSP/H.264 （转发）")

# ===== ② 边缘计算层 =====
band(392, 712, "②  边缘计算层 · 工控机（NVIDIA 独显 · Linux / Windows）", "#C0631E", "#FDF1E7")
box((LBX[0], 448, LBX[1], 648), "进程1 · AI 视觉诊断（主进程）",
    ["Python OpenCV/PyAV 拉主码流",
     "抽帧解耦   25fps → 5~8fps",
     "动态 ROI 裁剪（法兰盘锚点）",
     "TensorRT · YOLO 二分类（Class: Fault）",
     "滑动窗口 1.5s 时序平滑 → status(0/1)"],
    "#C0631E", "#9A4E12")
box((RBX0 := RCX - 340, 448, RCX + 340, 648), "进程2 · 视频旁路转发（后台）",
    ["FFmpeg 拉子码流",
     "-c:v copy  免编码（零重编码）",
     "推 RTMP 裸流至云端"],
    "#C0631E", "#9A4E12")
d.text(s(850, 672), "两进程物理隔离 · 崩溃自动重启 + 开机自启 · 托管：systemd (Linux) / NSSM (Windows)",
       font=f(16), fill="#7A4514", anchor="ma")

varrow(LCX, 648, 778, "MQTT / JSON  (QoS 1)")
varrow(RCX, 648, 778, "RTMP 裸流")

# ===== ③ 通讯链路层 =====
band(778, 968, "③  通讯链路层 · 双轨解耦", "#2E7D32", "#EAF6EC")
box((LBX[0], 832, LBX[1], 952), "通道 B · 数据流",
    ["MQTT Broker（阿里云 / 本地）",
     "QoS 1   ·   topic: rig/data/json"],
    "#2E7D32", "#1B5E20")
box((RCX - 340, 832, RCX + 340, 952), "通道 A · 视频流",
    ["云端 MediaMTX 流媒体服务器",
     "分发标准 RTMP 直播流"],
    "#2E7D32", "#1B5E20")

varrow(LCX, 952, 1042, "MQTT 订阅")
varrow(RCX, 952, 1042, "RTMP 订阅")

# ===== ④ 孪生应用层 =====
band(1042, 1290, "④  孪生应用层 · 上位机（LabVIEW · 远程订阅）", "#5E35B1", "#F1ECF9")
box((LBX[0], 1098, LBX[1], 1268), "数据驱动告警",
    ["订阅 MQTT · status=1 触发",
     "3D 卷筒模型故障态渲染",
     "声光报警 + 日志记录"],
    "#5E35B1", "#4527A0")
box((RCX - 340, 1098, RCX + 340, 1268), "视频人工复核",
    ["VLC 控件拉取 RTMP",
     "原画质裸流播放（无叠加）",
     "延迟 ≤ 5s 可接受"],
    "#5E35B1", "#4527A0")

img = img.resize((W, H), Image.LANCZOS)
img.save("docs/architecture.png")
print("saved docs/architecture.png", img.size)
