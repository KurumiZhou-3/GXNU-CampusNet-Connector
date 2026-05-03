import json
import os

import BaseVar
import GXLog


class ConfigFile:
    def __init__(self, configfile_path: str):
        self.configfile_path = configfile_path
        self.config_content_init = {"user_account": "",
                                    "user_password": "",
                                    "company": "",
                                    "direct_ip_address": "",
                                    "interface": "",
                                    "lang": ""
                                    }

        # The list of the config item can be set the default or 'Unknown' & not a bool-type config item
        self.not_necessary_config = ["direct_ip_address"]

        # The list of bool-type config item
        self.bool_type_config = []

        self.config_content_d = {}

        last_read = True

        # check config exist status
        if not os.path.isfile(self.configfile_path):
            GXLog.Data.wlog("No config file at this run path")
            GXLog.Data.wlog("Next to configure base setting ...")

            # created new config file
            self.file_init()
            self.content_init(list(self.config_content_init.keys()))

            # write back
            self.write()

            last_read = True
        else:
            GXLog.Data.slog("Config file is exist")

            empty_value_list, empty_item_list = self.read()
            if (self.config_content_d == {}) or (len(empty_value_list) != 0) or empty_item_list:
                # Get and Config the empty setting

                empty_total = [list(self.config_content_d.keys())[empty_index] for empty_index in
                               empty_value_list] + empty_item_list

                self.content_init(empty_total)

                # write back
                self.write()
            else:
                last_read = False

        if last_read:
            self.read()

    def file_init(self):
        """
        Created(or empty the old) a new config file with blank content
        :return:
        """
        if not os.path.isfile(self.configfile_path):
            # create a config file
            with open(self.configfile_path, 'w', encoding="utf-8") as configfile:
                configfile.write(json.dumps(self.config_content_init, indent=4))

    def content_init(self, loss_key: list):
        # self.config_content_d["user_account"] = input("Please input user account to created config:")
        # self.config_content_d["user_password"] = input("Please input password to created config:")
        #
        # print(BaseVar.CompanyChooseStr)
        # self.config_content_d["company"] = input("Input the number to choose net type:")
        for key in loss_key:
            if key != "company":
                self.set_value(key, "Please input value to set %s item to configure" % key)
            else:
                print(BaseVar.CompanyChooseStr)
                self.set_value(key, "Please choose the net supporter and input the number to configure",
                               limited_selection=["0", "1", "2", "3"])

    def read(self) -> tuple[list[int], list[str]]:
        """
        Read the stored information from config file
        :return:
        """
        with open(self.configfile_path, "r", encoding="utf-8") as configfile:
            self.config_content_d = json.load(configfile)

            empty_setting_list = []
            empty_item_list = []

            origin_content_d_keys = list(self.config_content_init.keys())

            # PrintLog out
            for index, value, key in zip(range(len(self.config_content_d)), self.config_content_d.values(),
                                         self.config_content_d.keys()):
                if key in origin_content_d_keys:

                    if value != "":
                        GXLog.Data.slog("Read successfully -> %s" % key)
                    else:
                        empty_setting_list.append(index)
                        GXLog.Data.wlog("The empty value setting -> %s" % key)

                    origin_content_d_keys.pop(origin_content_d_keys.index(key))
                else:
                    GXLog.Data.wlog("Unknown item key setting '%s'" % key)

            if origin_content_d_keys:
                for i in origin_content_d_keys:
                    GXLog.Data.wlog("Lack to configuration -> %s" % i)

            return empty_setting_list, origin_content_d_keys

    def write(self):
        """
        Write the information into config file
        :return:
        """
        with open(self.configfile_path, "w") as configfile:
            configfile.write(json.dumps(self.config_content_d, indent=4))

        GXLog.Data.slog("Store the config successfully")

    def set_value(self, config_content_d_key: str, msg: str,
                  default_content: str = "Unknown",
                  mode: str = "non-bool",
                  limited_selection: list = None
                  ):
        show_msg = True
        while show_msg:
            # Check mode
            if mode == "non-bool":
                # Check is it in the item had the default setting or just Bool
                if config_content_d_key not in self.not_necessary_config:
                    result = input(msg + ':')

                    if result and (not limited_selection or result in limited_selection):
                        self.config_content_d[config_content_d_key] = result
                        show_msg = False
                    else:
                        if result != "":
                            GXLog.Data.wlog("Please input the ALLOWED data")
                        else:
                            GXLog.Data.wlog("Please input AGAIN, this item need to be setting")
                else:
                    result = input(msg + '(Press ENTER to set the default):')

                    if result == "":
                        result = default_content
                        GXLog.Data.wlog("Setting the default '%s' into item '%s'" % (default_content, config_content_d_key))
                    self.config_content_d[config_content_d_key] = result
                    show_msg = False
            else:
                result = input(msg + "(Press ENTER to set 'y' or yES/nO):")
                if result in ["y", "yes", "yES", "yeS", "Y", "Yes", "YEs", "YES", ""]:
                    self.config_content_d[config_content_d_key] = "y"
                    show_msg = False
                else:
                    if result in ["n", "no", "nO", "N", "No", "NO"]:
                        self.config_content_d[config_content_d_key] = "n"
                        show_msg = False
                    else:
                        GXLog.Data.wlog("Please input the correct format data")


if __name__ == "__main__":
    import GXPath

    tmp_work_path = GXPath.get_local_path() + "/test.json"
    print(tmp_work_path)

    main = ConfigFile(tmp_work_path)
