import importlib.util


def _has(mod):
    return importlib.util.find_spec(mod) is not None


def available_backends():
    """返回当前机器可用的推理后端列表。"""
    backends = ["onnx"]  # onnxruntime 在 requirements 中, 视为基线
    if _has("openvino"):
        backends.append("openvino")
    try:
        import torch
        if torch.cuda.is_available():
            backends.append("tensorrt")
    except Exception:
        pass
    return backends


def export_targets(has_cuda):
    """返回应导出的格式列表。"""
    targets = ["onnx"]
    if _has("openvino"):
        targets.append("openvino")
    if has_cuda:
        targets.append("engine")
    return targets
