# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

from log import MyLogger

# 当前文件所在路径
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, "asserts")

IMG_DIR = os.path.join(STATIC_DIR, "imgs")

# 定义 IP 和端口号
HOST = "127.0.0.1"
PORT = 16542
main_config_file = os.path.join(BASE_DIR, "config.json")


class MyConfig:
    def __init__(self):
        self.is_init = False

    def init(self):
        try:
            global main_config_file
            with open(main_config_file, "r", encoding="utf-8") as f:
                self.config_data = json.loads(self.format_data(f.read()))
        except Exception as e:
            MyLogger.error("Reload Config File Error:{}".format(e))
            raise ValueError(" ")
        
    @classmethod
    def format_data(self, data: str):
        base_dir = str(BASE_DIR).replace("\\","\\\\")
        data = data.replace("$BASE_DIR", base_dir)
        return data

    def __getattr__(self, attr):
        if not self.is_init:
            self.init()
        if attr in self.config_data:
            return self._get_nested_dict(self.config_data[attr])
        else:
            return None

    def _get_nested_dict(self, data):
        if isinstance(data, dict):
            return NestedDict(data)
        if isinstance(data, list):
            return [NestedDict(i) for i in data]
        else:
            return data

    def __iter__(self):
        if not self.is_init:
            self.init()
        return iter(
            (key, self._get_nested_dict(value))
            for key, value in self.config_data.items()
        )


class NestedDict:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, attr):
        if attr in self.data:
            return self._get_nested_dict(self.data[attr])
        else:
            return None

    def __iter__(self):
        return iter(
            (key, self._get_nested_dict(value)) for key, value in self.data.items()
        )

    def _get_nested_dict(self, data):
        if isinstance(data, dict):
            return NestedDict(data)
        if isinstance(data, list):
            return [NestedDict(i) for i in data]
        else:
            return data

    def __str__(self) -> str:
        return str(self.data)


config = MyConfig()
