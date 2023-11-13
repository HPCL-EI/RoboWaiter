import os

def get_root_path():
    return os.path.abspath(
        os.path.join(__file__, "../../..")
    )
