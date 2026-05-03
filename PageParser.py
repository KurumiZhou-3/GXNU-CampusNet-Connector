import pprint
from io import StringIO

from bs4 import BeautifulSoup

import BaseVar


def base_script_parser(script_str: str) -> list[str]:
    # True into fileobj to use readlines()
    fileio = StringIO(script_str)
    script_in_lines = fileio.readlines()

    tmp_lines = []

    for i, content in enumerate(script_in_lines):
        # Remove the meaningless elements
        content = content.replace(" \n", "").replace("\n", "").replace(" ", "")

        # Remove the subscription
        if content[:2] == "//" or content == '' or content[:2] == "/*":
            continue

        # Cut into piece by ";"
        tmp_lines_content = content.split(";")

        for index, single_var in enumerate(tmp_lines_content):
            var_name = single_var[:single_var.find("=")]  # Get single var name

            # Get the url var out
            if ("v6" not in var_name) and ("v4" not in var_name) and ("domain" not in var_name):

                # Remove the double slash if there are lots of it
                while 1:
                    if "//" in single_var:
                        single_var = single_var[:single_var.rfind("//")]
                    else:
                        break

                # Deal with special case
                if var_name == "mip" or var_name == 'Gno':
                    single_var = single_var.replace("=", "='") + "'"

            tmp_lines_content[index] = single_var  # Write back to list

        tmp_content = tmp_lines_content
        tmp_content2 = tmp_content if tmp_content[-1] != "" else tmp_content[:-1]

        # Cut in piece and Flat the list which include the ","
        tmp_lines += sum([result.split(",") if "," in result and result[:6 + 1] != "carrier" else [result] for result in
                          tmp_content2], [])

    return [result for result in tmp_lines if result != "/"]


def parse_data(unparsed_data: str, mode="onlytitle") -> list[str | dict]:
    """
    mode(default) = "onlytitle" --return--> [title_str]
    mode = "all" or the other  --return--> [title_str, [ [info_list1], [info_list2] ... ] ]

    :param unparsed_data:
    :param mode:
    :return:
    """
    # 创建 BeautifulSoup 对象
    soup = BeautifulSoup(unparsed_data, 'lxml')

    script_list = []

    # 获取网页的 title
    title = soup.find('title').get_text()

    if mode != "onlytitle":
        # 获取特定标签的值
        # 获取 前两个 <script> 标签的文本内容
        li_tags = soup.find_all('script')
        # print(len(li_tags))

        for idx, li in enumerate(li_tags, 1):
            if idx == 2:
                break
            script_list.append(li.get_text())  # 存储内容

        # Get command list
        command_list = [base_script_parser(script_list_content.replace("\r", "")) for script_list_content in
                        script_list]

        result_dict = {}  # Init the result_dict to store var dict

        # True info into dict
        for command_floor1 in command_list:
            for command in command_floor1:
                # Run command by exec()
                exec(command.replace("'", "") if "flow=" in command or "fee=" in command else command, globals())

                command_var_name = command[:command.find("=")]
                result_dict[command_var_name] = globals().get(command_var_name, "UNKNOWN")

        return [title, result_dict]

    else:
        return [title]


if __name__ == "__main__":
    import requests

    # 获取网页 Html 文件
    response = requests.get("https://yc.gxnu.edu.cn/", headers=BaseVar.GeneralHeaders)
    html_content = response.text

    pprint.pprint(parse_data(html_content, "withcontent"))
