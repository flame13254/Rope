import os
from rope_train.dummy_data import make_dummy_dataset, make_dummy_patches

def test_make_dataset_creates_class_folders(tmp_path):
    root = str(tmp_path / "ds")
    make_dummy_dataset(root, n_train=3, n_val=2)
    for split, n in (("train", 3), ("val", 2)):
        for cls in ("normal", "fault"):
            d = os.path.join(root, split, cls)
            assert os.path.isdir(d)
            assert len(os.listdir(d)) == n

def test_make_patches(tmp_path):
    d = str(tmp_path / "patches")
    make_dummy_patches(d, n=4)
    assert len(os.listdir(d)) == 4
