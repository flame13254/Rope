# export.py
from ultralytics import YOLO

def export_model():
    # 加载训练好的最佳权重
    model = YOLO('runs/train/rope_obb_v1/weights/best.pt')

    # 导出为 TensorRT engine
    # half=True 表示启用 FP16 半精度推理，进一步加速
    model.export(format='engine', device=0, half=True, dynamic=False)
    print("Export Complete. Look for the .engine file.")

if __name__ == '__main__':
    export_model()