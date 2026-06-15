# train.py
from ultralytics import YOLO

def train_model():
    # 1. 加载预训练的 YOLOv8-OBB 模型 (推荐使用 nano 或 small 版本开始)
    model = YOLO('yolov8n-obb.pt')

    # 2. 开始训练
    results = model.train(
        data='rope.yaml',        # 数据集配置文件
        epochs=100,              # 训练轮数
        imgsz=640,               # 图像大小 (训练时图像会被缩放到此尺寸)
        batch=16,                # 批次大小 (根据显存调整)
        device=0,                # 使用的 GPU (0 表示第一块 GPU)
        name='rope_obb_v1',      # 保存的实验名称
        project='runs/train'     # 保存结果的目录
    )
    print("Training Complete. Weights saved in 'runs/train/rope_obb_v1/weights/'")

if __name__ == '__main__':
    train_model()