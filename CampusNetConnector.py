import argparse
import json
import sys

import requests

import BaseVar
import Configurator
import GXLog
import GXNet
import GXPath
import PageParser
import toolkit

VERSION = "0.0.3"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="CampusNetConnector",
        description="GXNU (广西师范大学) 校园网 CLI 认证程序",
    )
    parser.add_argument(
        "--list-interfaces", action="store_true",
        help="列出所有检测到的网络接口后退出",
    )
    parser.add_argument(
        "--direct-ip", action="store_true",
        help="直连 IP 模式，使用配置中的 direct_ip_address 并跳过 SSL 验证",
    )
    parser.add_argument(
        "--config", action="store_true",
        help="仅运行交互式配置向导，不执行登录/注销",
    )
    parser.add_argument(
        "--log-file", type=str, metavar="PATH",
        help="启用文件日志持久化，日志追加写入指定文件",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="查询当前认证状态和会话信息",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {VERSION}",
    )
    return parser.parse_args()


class Main:
    def __init__(self, use_direct_ip: bool = False):
        # 基本路径
        self.run_env_path = GXPath.end_with_slash(GXPath.get_local_path())
        self.configfile_path = self.run_env_path + "CampusNetConfig.json"
        self.configurator = Configurator.ConfigFile(self.configfile_path)

        # 直连 IP 模式
        self.verify_mode = True
        if use_direct_ip:
            direct_ip = self.configurator.config_content_d["direct_ip_address"]
            BaseVar.main_url = f"https://{direct_ip}/"
            self.verify_mode = False

        # 从配置读取参数
        self.user_account = self.configurator.config_content_d["user_account"]
        self.user_password = self.configurator.config_content_d["user_password"]
        self.company = self.configurator.config_content_d["company"]
        self.lang = self.configurator.config_content_d["lang"]
        self.lang2 = self.lang[:2]
        self.interface_name = self.configurator.config_content_d["interface"]

        # 运行时状态
        self.login_ipv4_addr = ""
        self.login_ipv6_addr = ""
        self.user_real_name = ""
        self.wlan_user_mac = ""

        # 检测登录状态并执行登录或注销
        login_status = self._status_init()
        if not login_status:
            self._login(self.user_account, self.user_password, self.company)
        else:
            self._logout(self.interface_name)

    def _status_init(self) -> bool:
        resp = requests.get(BaseVar.main_url, headers=BaseVar.GeneralHeaders, verify=self.verify_mode)
        title = PageParser.parse_data(resp.text, mode="onlytitle")[0]
        GXLog.Net.slog(f"The web login status: {title}")
        return title == "注销页"

    def _login(self, user_account: str, password: str, company: str) -> bool:
        GXLog.Net.slog("Start login ...")
        BaseVar.main_url_login = BaseVar.main_url

        login_page = requests.get(BaseVar.main_url_login, headers=BaseVar.GeneralHeaders, verify=self.verify_mode).text
        parsed_data = PageParser.parse_data(login_page, mode="parseAll")[1]

        url_data = toolkit.get_login_url_arg(
            BaseVar.CallBack.login,
            user_account, password, company,
            parsed_data["v46ip"], self.login_ipv6_addr,
            BaseVar.terminal_type, self.lang,
            str(toolkit.get_v_random()), self.lang2,
            BaseVar.jsVersion,
        )

        login_url = toolkit.get_login_url(BaseVar.main_url_login, url_data)
        login_result = requests.get(login_url, headers=BaseVar.GeneralHeaders, verify=self.verify_mode).text[12:-4]
        login_result_json = json.loads(login_result)

        self.login_ipv4_addr = login_result_json["v46ip"]
        self.user_real_name = login_result_json["NID"]
        self.wlan_user_mac = login_result_json["olmac"]

        if login_result_json["result"] == 1:
            GXLog.Net.slog("Login successfully")
            return True
        else:
            GXLog.Net.elog("Login Failed")
            return False

    def _logout(self, interface_name: str) -> bool:
        GXLog.Net.slog("Start logout the campus net ...")

        if interface_name:
            GXLog.Net.slog(f"Get the IPv4 address from interface {interface_name}")
            my_ipv4 = GXNet.Interface.get_detail_interface_ipv4(interface_name)
        else:
            my_ipv4 = self.login_ipv4_addr

        url_data = toolkit.get_logout_url_arg(
            BaseVar.CallBack.logout,
            BaseVar.Logout.logout_method, BaseVar.Logout.user_account,
            BaseVar.Logout.user_password, BaseVar.Logout.ac_logout,
            BaseVar.Logout.register_mode, my_ipv4, self.login_ipv6_addr,
            BaseVar.Logout.wlan_vlan_id, self.wlan_user_mac,
            BaseVar.Logout.wlan_ac_ip, BaseVar.Logout.wlan_ac_name,
            BaseVar.jsVersion, str(toolkit.get_v_random()), self.lang2,
        )

        logout_host = BaseVar.main_url[:-1] + ":802/"
        GXLog.Net.slog(f"Logout host: {logout_host}")
        logout_url = toolkit.get_logout_url(logout_host, url_data)
        logout_text = requests.get(logout_url, headers=BaseVar.GeneralHeaders, verify=self.verify_mode).text[7:-2]
        logout_result = json.loads(logout_text)

        if logout_result["result"] == 1:
            GXLog.Net.slog(f"Logout successfully, msg: {logout_result['msg']}")
            return True
        else:
            GXLog.Net.elog("Logout Failed")
            return False


_ISP_NAMES = {0: "校园网", 1: "中国电信", 2: "中国联通", 3: "中国移动"}


def show_status():
    """查询当前认证状态，已登录时展示会话详情。"""
    print("正在查询认证状态 ...\n")
    resp = requests.get(BaseVar.main_url, headers=BaseVar.GeneralHeaders, verify=True)
    title, data = PageParser.parse_data(resp.text, mode="parseAll")

    is_logged_in = title == "注销页"
    print(f"  认证状态: {'已登录' if is_logged_in else '未登录'}（{title}）")

    if not is_logged_in:
        return

    # 从页面脚本中提取会话字段
    uid = data.get("uid", "").strip("'")
    nid = data.get("NID", "").strip("'")
    v4ip = data.get("v4ip", "").strip("'")
    v6ip = data.get("v6ip", "").strip("'")
    stime = data.get("stime", "").strip("'")
    etime = data.get("etime", "").strip("'")
    flow = str(data.get("flow", "")).strip().strip("'")
    oltime = data.get("oltime", 0)
    olflow = data.get("olflow", 0)
    ispid = data.get("ispid", "")

    # 格式化
    MAX_UINT32 = 4294967295
    isp_name = _ISP_NAMES.get(ispid, f"未知({ispid})")
    time_limit = "无限制" if oltime == MAX_UINT32 else str(oltime)
    flow_limit = "无限制" if olflow == MAX_UINT32 else f"{olflow}"

    print(f"  账    号: {uid}")
    print(f"  姓    名: {nid}")
    print(f"  运 营 商: {isp_name}")
    print(f"  IPv4 地址: {v4ip}")
    print(f"  IPv6 地址: {v6ip}")
    print(f"  登录时间: {stime}")
    print(f"  过期时间: {etime}")
    print(f"  在线时长: {time_limit}")
    print(f"  流量上限: {flow_limit}")
    if flow:
        print(f"  已用流量: {flow}")


def main():
    args = _parse_args()

    if args.log_file:
        GXLog.enable_file_log(args.log_file)
        GXLog.Net.slog(f"File logging enabled: {args.log_file}", mode="notime")

    if args.list_interfaces:
        print("All Network Interfaces detected:\n")
        for i, name in enumerate(GXNet.Interface.get_local_net_interface_name(), 1):
            print(f"  {i}) {name}")
        sys.exit(0)

    if args.config:
        config_path = GXPath.end_with_slash(GXPath.get_local_path()) + "CampusNetConfig.json"
        Configurator.ConfigFile(config_path)
        sys.exit(0)

    if args.status:
        show_status()
        sys.exit(0)

    Main(use_direct_ip=args.direct_ip)


if __name__ == "__main__":
    main()
