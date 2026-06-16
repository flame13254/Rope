from rope_train.config import load_experiments, resolve_device

def test_load_experiments_has_four_runs():
    runs = load_experiments("configs/experiments.yaml")
    assert len(runs) == 4
    names = {r["name"] for r in runs}
    assert names == {"v8s-cls-320", "v8s-cls-640", "v8n-cls-320", "v8n-cls-640"}

def test_common_merged_into_each_run():
    runs = load_experiments("configs/experiments.yaml")
    r = runs[0]
    assert r["epochs"] == 100 and r["data"] == "dataset_cls"
    assert r["imgsz"] in (320, 640)

def test_resolve_device_auto_returns_valid():
    assert resolve_device("auto") in ("0", "cpu")
    assert resolve_device("cpu") == "cpu"
