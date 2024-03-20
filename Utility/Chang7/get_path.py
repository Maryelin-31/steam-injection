# -*- coding: utf-8 -*-


from zml import make_parent
from zmlx.alg.join_paths import join_paths
import os


def get_path(*args):
    return make_parent(join_paths(os.path.dirname(__file__), *args))


if __name__ == "__main__":
    print(get_path())
