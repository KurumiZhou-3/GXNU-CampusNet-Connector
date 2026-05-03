"""
网络接口检测模块，基于 psutil 获取本机 IPv4 地址。
用于校园网认证时获取本机 IP，以及 list-interface-name 模式列出所有接口。
"""
import socket
import psutil


class Interface:
    @staticmethod
    def get_local_net_interface_name() -> list:
        """返回所有网络接口名称列表。"""
        return list(psutil.net_if_addrs().keys())

    @staticmethod
    def get_ipv4_interface() -> dict:
        """
        返回所有含 IPv4 地址的接口，格式 {接口名: snicaddr 对象}。
        每个接口只取第一个 IPv4 地址。
        """
        ipv4_dict = {}
        for name, addrs in psutil.net_if_addrs().items():
            ipv4_addrs = [addr for addr in addrs if addr.family == socket.AF_INET]
            if ipv4_addrs:
                ipv4_dict[name] = ipv4_addrs[0]
        return ipv4_dict

    @staticmethod
    def get_detail_interface_ipv4(interface_name: str) -> str | None:
        """获取指定接口的 IPv4 地址，不存在时返回 None。"""
        addr = Interface.get_ipv4_interface().get(interface_name)
        return addr.address if addr else None
