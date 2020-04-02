# coding: utf-8

""""""

import os

# 从setting目录向上推,获取django3template项目根目录路径
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))
