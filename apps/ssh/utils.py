import json
import os

from kernel.settings import config, MyConfig


class SshUtils:
    def __init__(self) -> None:
        pass

    def load_data(self, *args, **kwargs):
        with open(config.ssh.commands, "r", encoding="utf-8") as f:
            data = f.read()
        data = json.loads(MyConfig.format_data(data))
        data = [{"text": key, "details": value} for key, value in data.items()]
        return data

    def ssh(self, conf, *args, **kwargs):
        pem = conf.get("pem", None)
        password = conf.get("pwd", "None")
        host = conf["host"]
        if password:
            ssh = f"ssh {host}"
        if pem:
            ssh = f"ssh -i {pem} {host}"

        try:
            os.system(f" start cmd.exe /K {ssh}")
        except Exception as e:
            print(e)
