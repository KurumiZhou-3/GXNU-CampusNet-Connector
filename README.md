# GXNU-CampusNet-Connector

广西师范大学 (GXNU) 校园网 CLI 认证客户端，通过 `yc.gxnu.edu.cn` 门户实现自动登录/注销。可用于软路由等无人值守环境，支持定时任务集成。

## 安装

```bash
pip install requests beautifulsoup4 lxml psutil
```

Python 3.10+ 均可运行，开发环境为 Python 3.13。

## 用法

```bash
# 登录或注销（自动检测当前状态并切换）
python CampusNetConnector.py

# 查询当前认证状态和会话信息
python CampusNetConnector.py --status

# 仅运行交互式配置向导
python CampusNetConnector.py --config

# 直连 IP 模式（跳过 SSL 验证，用于绕过 DNS/证书问题）
python CampusNetConnector.py --direct-ip

# 列出所有网络接口
python CampusNetConnector.py --list-interfaces

# 启用文件日志（适合定时任务场景）
python CampusNetConnector.py --log-file /var/log/campusnet.log
```

## 配置

首次运行会自动进入交互式配置向导，生成 `CampusNetConfig.json`：

| 字段 | 说明 |
| --- | --- |
| `user_account` | 学号/工号 |
| `user_password` | 校园网密码（明文存储，注意文件权限） |
| `company` | 运营商: `0`=校园网, `1`=中国电信, `2`=中国联通, `3`=中国移动 |
| `interface` | 连接校园网的网络接口，用于获取本机 IP（如 `eth0`, `wlan0`） |
| `direct_ip_address` | 直连 IP 模式的备用地址（可选）。当无法通过当前DNS（非学校DNS）解析认证网站IP或出现SSL证书问题的时候可设置该项以使用指定的IP操作，育才校区通常为`192.50.125.13` |
| `lang` | 语言，默认 `zh-cn` |

## 认证流程

1. GET `https://yc.gxnu.edu.cn/`，解析 `<title>` 判断登录状态（"上网登录页" = 未登录，"注销页" = 已登录）
2. 未登录时：从页面 `<script>` 标签提取认证参数（v4ip、v6ip 等），拼接登录 URL 并发送 GET 请求
3. 已登录时：获取本机 IPv4 地址，向 `https://yc.gxnu.edu.cn:802/` 发送注销请求

## 项目结构

| 文件 | 职责 |
| --- | --- |
| `CampusNetConnector.py` | 主入口，CLI 解析与认证流程编排 |
| `BaseVar.py` | 常量定义：门户 URL、HTTP 请求头、URL 路径模板 |
| `PageParser.py` | 解析门户页面，提取 `<title>` 和 `<script>` 中的 JS 变量 |
| `toolkit.py` | URL 参数构建、随机数生成 |
| `GXNet.py` | 基于 psutil 的网络接口检测，获取本机 IPv4 地址 |
| `GXLog.py` | 彩色终端日志，支持文件持久化 |
| `GXPath.py` | 路径工具函数 |
| `Configurator.py` | 交互式 JSON 配置文件管理 |

## 许可

MIT
