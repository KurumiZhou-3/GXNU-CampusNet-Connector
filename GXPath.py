"""
路径工具模块，用于获取脚本所在目录和路径规范化。
"""
import os


def get_local_path() -> str:
    """返回脚本文件所在目录的绝对路径。使用 __file__ 确保不受启动方式影响。"""
    return os.path.dirname(os.path.realpath(__file__))


def end_with_slash(path: str) -> str:
    """确保路径以平台原生路径分隔符结尾（Windows=\\，Unix=/）。"""
    return path if path.endswith(os.sep) else path + os.sep
