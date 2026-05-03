import random

# CampusNet Portal Part
hostname_campus_net = "yc.gxnu.edu.cn"
main_url = "https://yc.gxnu.edu.cn/"
main_url_login = main_url
# main_url_logout = "https://yc.gxnu.edu.cn:802/"
main_url_logout = main_url[:-1]+":802/"
terminal_type = "1"
jsVersion = "4.2.2"

# Other Part

GeneralHeaders = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'Accept-Encoding': "gzip, deflate, br, zstd",
    'Accept-Language': "zh,zh-CN;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'DNT': '1',
    'Host': hostname_campus_net,
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': "?1",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows"
}

CompanyChooseStr = """
Choose one net type:
    0) CampusNetwork (校园网)
    1) China Telecom (中国电信)
    2) China Unicom (中国联通)
    3) China Mobile (中国移动)
"""

class Filename:
    login = "drcom/login?"
    logout = "eportal/portal/logout?"
    # unbind = "eportal/portal/mac/unbind?"


class Login:
    main_url = main_url_login
    filename = Filename.login


class Logout:
    main_url = main_url_logout
    filename = Filename.logout

    logout_method = '0'
    user_account = "drcom"
    user_password = "123"
    ac_logout = "1"
    register_mode = '1'

    wlan_vlan_id = '1'
    wlan_user_mac = '000000000000'
    wlan_ac_ip = ''
    wlan_ac_name = ''


class CallBack:
    login = "dr1004"
    login_successfully = "dr1001"
    logoutList = ["dr1006", 'dr1002', 'dr1003']

    logout = logoutList[random.randint(0, 2)]
