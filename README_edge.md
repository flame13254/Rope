# 边缘端使用说明（Phase 2）

## 安装
pip install -r requirements.txt   # 含 paho-mqtt; 可选 openvino

## 两个进程
- AI 主进程: `python edge_main.py --config configs/edge.yaml`
- 转发进程: `python forward.py --config configs/edge.yaml`

## 验证(无摄像头/broker/模型)
- `python edge_main.py --max-frames 30`   # 合成源+Mock分类器+日志发布, 打印 status JSON
- `python forward.py --dry-run`           # 打印 ffmpeg 命令
- `python -m pytest -q`                    # 全部单元测试

## 切换到真实环境(改 configs/edge.yaml, 不改代码)
- source.type: rtsp, source.path: 摄像头主码流 RTSP URL
- model.type: yolo, model.path: Phase1 导出的模型(best.pt/.onnx/.engine/openvino)
- mqtt.enabled: true, 填 host/port
- forward.sub_url/rtmp_url: 子码流与云端 RTMP 地址
- frame_stride: 默认3(源:推理=3:1); 硬件吃紧调大
- roi: 现场标定固定矩形(动态ROI锚点为后续接口)

## 部署
- Linux: 复制 deploy/*.service 到 /etc/systemd/system/, systemctl enable --now
- Windows: 以管理员运行 deploy/nssm-install.ps1
