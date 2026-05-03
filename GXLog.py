"""
彩色终端日志模块，支持同时输出到文件和终端。
使用方式: GXLog.Net.slog("info") / GXLog.Data.wlog("warn") / GXLog.Net.elog("error")
文件日志默认关闭，调用 enable_file_log(path) 开启持久化。
"""
import datetime
import os
import sys

# 日志前缀符号：成功=# 警告=? 错误=!
STANDARD_OUTPUT_SYMBOL = "#"
WARNING_SYMBOL = "?"
ERROR_SYMBOL = "!"

# 日志域名称
NET_PART_NAME = "net"
DATASTORE_PART_NAME = "data"

_log_file_path: str | None = None

# 当 stdout 是终端且未设置 NO_COLOR 环境变量时启用 ANSI 颜色
_USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

_COLORS = {
    "green": "\033[1;32m",   # 成功：粗体绿
    "yellow": "\033[1;33m",  # 警告：粗体黄
    "red": "\033[1;31m",     # 错误：粗体红
    "reset": "\033[0m",      # 重置
}


def enable_file_log(file_path: str):
    """启用文件日志持久化（纯文本追加写入），自动创建父目录。"""
    global _log_file_path
    _log_file_path = file_path
    _log_dir = os.path.dirname(file_path)
    if _log_dir and not os.path.isdir(_log_dir):
        os.makedirs(_log_dir, exist_ok=True)


def _cprint(color: str, text: str):
    """终端输出，TTY 时带 ANSI 颜色，管道时纯文本。"""
    if _USE_COLOR:
        print(f"{_COLORS[color]}{text}{_COLORS['reset']}")
    else:
        print(text)


def _format_msg(symbol: str, part: str, text: str, with_time: bool) -> str:
    """构造日志前缀，格式: [#net 2020-04-13 17:09:49] message"""
    prefix = f"[{symbol}{part}"
    if with_time:
        prefix += f" {datetime.datetime.now()}"
    return f"{prefix}] {text}"


def _log(color: str, text: str, symbol: str, part: str, mode: str):
    """统一日志出口：终端输出 + 可选文件写入。"""
    msg = _format_msg(symbol, part, text, mode == "withtime")
    _cprint(color, msg)
    if _log_file_path:
        with open(_log_file_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")


# ---- 底层日志函数（Net / Data 类通过 _DomainLogger 调用）----

def slog(output_text: str, front_symbol: str, front_text: str, mode: str = "withtime"):
    _log("green", output_text, front_symbol, front_text, mode)


def wlog(output_text: str, front_symbol: str, front_text: str, mode: str = "withtime"):
    _log("yellow", output_text, front_symbol, front_text, mode)


def elog(output_text: str, front_symbol: str, front_text: str, mode: str = "withtime"):
    _log("red", output_text, front_symbol, front_text, mode)


# ---- 领域日志类（对外的 API 入口）----

class _DomainLogger:
    """领域日志基类，子类只需定义 _symbol 和 _name。"""
    _symbol = ""
    _name = ""

    @classmethod
    def slog(cls, output_text: str, mode: str = "withtime"):
        _log("green", output_text, cls._symbol, cls._name, mode)

    @classmethod
    def wlog(cls, output_text: str, mode: str = "withtime"):
        _log("yellow", output_text, cls._symbol, cls._name, mode)

    @classmethod
    def elog(cls, output_text: str, mode: str = "withtime"):
        _log("red", output_text, cls._symbol, cls._name, mode)


class Net(_DomainLogger):
    """网络相关日志，前缀 [#net]。"""
    _symbol = STANDARD_OUTPUT_SYMBOL
    _name = NET_PART_NAME


class Data(_DomainLogger):
    """数据/配置相关日志，前缀 [#data]。"""
    _symbol = STANDARD_OUTPUT_SYMBOL
    _name = DATASTORE_PART_NAME
