from rope_train.backends import available_backends, export_targets

def test_onnx_always_available():
    assert "onnx" in available_backends()

def test_export_targets_excludes_engine_without_cuda():
    assert "engine" not in export_targets(has_cuda=False)
    assert "onnx" in export_targets(has_cuda=False)

def test_export_targets_includes_engine_with_cuda():
    assert "engine" in export_targets(has_cuda=True)
