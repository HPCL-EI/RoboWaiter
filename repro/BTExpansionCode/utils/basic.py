import os

# 返回本实验存档的父目录（当前为 repro/），供 utils/bt/load.py 拼接
# "BTExpansionCode/EXP/behavior_lib" 等路径；注意它不是仓库根目录。

def get_root_path():
    return os.path.abspath(
        os.path.join(__file__, "../../..")
    )
