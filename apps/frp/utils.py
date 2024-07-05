import subprocess


from kernel.settings import config
from log import MyLogger


class FrpUtils:
    def __init__(self) -> None:
        pass

    def check_service(self, *args, **kwargs):
        import psutil

        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] == config.frpc.name:
                return True
        return False

    def open_config(self, *args, **kwargs):
        subprocess.Popen(["cmd", "/c", "start", "", f"{config.frpc.toml}"], shell=True)

    def stop_service(self, *args, **kwargs):
        subprocess.Popen(
            ["cmd", "/c", "taskkill", "/f", "/im", f"{config.frpc.name}"], shell=True
        )
        MyLogger.info("frpc.exe shutdown!")

    def start_service(self):
        # 创建一个 STARTUPINFO 对象，设置参数使命令行窗口隐藏
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "/B",
                "cmd",
                "/c",
                f"{config.frpc.exe} -c {config.frpc.toml}",
            ],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        MyLogger.info("frpc.exe start!")
