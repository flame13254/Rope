# 训练侧使用说明（Phase 1）

图像分类（正常/故障 → 0/1）训练框架，对比 YOLOv8s-cls 与 YOLOv8n-cls × {320, 640}。

## 安装
```
pip install -r requirements.txt
# 可选后端：pip install openvino        # Intel 机器
#           pip install tensorrt        # NVIDIA 机器（或随 CUDA 安装）
```
> 注：`onnx` 锁定 `<1.17`，1.17 在部分 Windows/conda 环境会出现 `onnx_cpp2py_export` DLL 初始化失败。

## 流程
1. **准备数据**：真实数据按下面结构放置；无数据时先生成合成集验证管线。
   ```
   dataset_cls/
     train/{normal,fault}/*.jpg
     val/{normal,fault}/*.jpg
   ```
   合成验证：`python tools/make_dummy_dataset.py`
2. **（可选）造故障样本**（方案第八节 Copy-Paste）：
   `python tools/copy_paste_aug.py --count 200`
   （把 `patches/` 里的真实故障小块随机贴到正常背景，存为 fault 类；禁用大角度旋转）
3. **训练全部 4 个 run**：`python train.py`
   - 冒烟：`python train.py --only v8n-cls-320 --smoke-epochs 1`
   - 在线增强已开启光度扰动抗环境光，`degrees=0` 禁大角度旋转。
4. **导出多后端**：`python export.py`
   - `onnx` 通用（CPU/ONNXRuntime）；检测到 `openvino`/CUDA 时额外导出 `openvino`/`engine`(FP16)，缺失则跳过并告警。
5. **基准对比**：`python benchmark.py`
   - 输出 `runs/benchmark.md` + `runs/benchmark.csv`（fault 类 F1 / 单帧 ms / 内存 MB），据此选最终模型 + 分辨率。

## 实验配置
编辑 `configs/experiments.yaml` 增删 run。`device: auto` 自动选 GPU/CPU。

## 产物路径
Ultralytics 分类模式会把结果存到 `runs/classify/runs/<name>/weights/best.pt`（含 `classify/` 子目录）。`export.py`/`benchmark.py` 通过 `find_best()` 自动定位，无需关心该嵌套。

## 测试
`python -m pytest -q`　（纯逻辑测试，无需联网/GPU）

## 范围
本框架仅含训练/导出/基准；边缘推理、FFmpeg 转发、MQTT、上位机为 Phase 2。
