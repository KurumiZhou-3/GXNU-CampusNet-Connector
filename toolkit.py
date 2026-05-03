import random
from urllib.parse import urlencode

import BaseVar


def get_v_random() -> int:
    return random.randint(500, 10499)


def get_login_url_arg(callback: str, user_account: str, password: str, company: str,
                      v4ip: str, v6ip: str, terminal_type: str, lang: str, v: str,
                      lang2: str, js_version: str) -> str:
    data = {
        "callback": callback,
        "DDDDD": user_account,
        "upass": password,
        "0MKKey": "123456",
        "R1": "0",
        "R2": "",
        "R3": company,
        "R6": "1",
        "para": "00",
        "v4ip": v4ip,
        "v6ip": v6ip,
        "terminal_type": terminal_type,
        "lang": lang,
        "jsVersion": js_version,
        "v": v,
    }
    return urlencode(data) + f"&lang={lang2}"


def get_logout_url_arg(callback: str, login_method: str, user_account: str,
                       user_password: str, ac_logout: str, register_mode: str,
                       wlan_user_ip: str, wlan_user_ipv6: str, wlan_vlan_id: str,
                       wlan_user_mac: str, wlan_ac_ip: str, wlan_ac_name: str,
                       js_version: str, v: str, lang2: str) -> str:
    data = {
        "callback": callback,
        "login_method": login_method,
        "user_account": user_account,
        "user_password": user_password,
        "ac_login": ac_logout,
        "register_mode": register_mode,
        "wlan_user_ip": wlan_user_ip,
        "wlan_user_ipv6": wlan_user_ipv6,
        "wlan_vlan_id": wlan_vlan_id,
        "wlan_user_mac": wlan_user_mac,
        "wlan_ac_ip": wlan_ac_ip,
        "wlan_ac_name": wlan_ac_name,
        "jsVersion": js_version,
        "v": v,
        "lang": lang2,
    }
    return urlencode(data)


def get_login_url(main_host_name_with_slash: str, input_url_data: str) -> str:
    return f"{main_host_name_with_slash}{BaseVar.Filename.login}{input_url_data}"


def get_logout_url(main_host_name_with_slash: str, input_url_data: str) -> str:
    return f"{main_host_name_with_slash}{BaseVar.Filename.logout}{input_url_data}"
