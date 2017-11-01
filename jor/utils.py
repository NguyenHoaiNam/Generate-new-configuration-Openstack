# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

import logging
import os


def get_root_path(*directory):
    root_path = os.path.dirname(os.path.abspath(__file__))
    if directory is None:
        return root_path
    else:
        return os.path.join(root_path, *directory)


def get_log(name):
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(name)
