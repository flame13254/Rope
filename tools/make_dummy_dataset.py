"""生成合成分类数据集与故障小块, 仅用于验证管线。"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rope_train.dummy_data import make_dummy_dataset, make_dummy_patches


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="dataset_cls")
    ap.add_argument("--patches", default="patches")
    ap.add_argument("--n-train", type=int, default=20)
    ap.add_argument("--n-val", type=int, default=6)
    a = ap.parse_args()
    make_dummy_dataset(a.root, a.n_train, a.n_val)
    make_dummy_patches(a.patches)
    print(f"dummy 数据集 -> {a.root}, 故障小块 -> {a.patches}")


if __name__ == "__main__":
    main()
