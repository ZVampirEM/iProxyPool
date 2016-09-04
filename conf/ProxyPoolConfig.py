import json

CONFIG_FILE = "./conf/conf.json"

class ConfigOperating(object):
    def __init__(self):
        self.__m_headers = {}
        self.__m_url = ""
        self.__m_time_stamp = {}
        self.__m_listen_addr = ""
        self.__m_listen_port = ""
        self.__m_savefile_name = ""
#        self.__m_variablefile_name = ""
        self.__m_filter_headers = {}
        self.__m_filter_url_1 = ""
        self.__m_filter_url_2 = ""
        self.__m_filter_url_3 = ""
        self.parse_conf_json()

    def parse_conf_json(self):
        conf_json_obj = json.load(file(CONFIG_FILE))
        self.__m_headers = conf_json_obj["headers"]
        self.__m_url = conf_json_obj["url"]
        self.__m_time_stamp = conf_json_obj["time_stamp"]
        self.__m_listen_addr = conf_json_obj["listen_addr"]
        self.__m_listen_port = conf_json_obj["listen_port"]
        self.__m_savefile_name = conf_json_obj["savefile_name"]
        # self.__m_variablefile_name = conf_json_obj["varifile_name"]
        self.__m_filter_headers = conf_json_obj["filter_headers"]
        self.__m_filter_url_1 = conf_json_obj["filter_url_1"]
        self.__m_filter_url_2 = conf_json_obj["filter_url_2"]
        self.__m_filter_url_3 = conf_json_obj["filter_url_3"]

    @property
    def get_headers(self):
        return self.__m_headers

    @property
    def get_url(self):
        return self.__m_url

    @property
    def get_time_stamp(self):
        return self.__m_time_stamp

    @property
    def get_listen_addr(self):
        return self.__m_listen_addr

    @property
    def get_listen_port(self):
        return self.__m_listen_port
    @property
    def get_savefile_name(self):
        return self.__m_savefile_name

    # @property
    # def get_varifile_name(self):
    #     return self.__m_variablefile_name
    
    @property
    def get_filter_headers(self):
        return self.__m_filter_headers
    
    @property
    def get_filter_url_1(self):
        return self.__m_filter_url_1

    @property
    def get_filter_url_2(self):
        return self.__m_filter_url_2

    @property
    def get_filter_url_3(self):
        return self.__m_filter_url_3

config_instance = ConfigOperating()
