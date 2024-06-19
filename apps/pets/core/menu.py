import subprocess

import psutil

from apps.frp.utils import FrpUtils
from apps.myhttp.utils import MyHttpUtil
from apps.ssh.utils import SshUtils
from kernel.common import open_config_file
from kernel.events import StopEvents
from kernel.settings import config

from .base import BaseMenu, BasePetMaster
from .log import PetLogger
from .weight.mydraw import TextPopup


class FrpMenu(BaseMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_command(
            label="开启服务", command=self.start_service, foreground="green"
        )
        self.add_command(label="检查是否存活", command=self.check_service)
        self.add_command(label="关闭服务", command=self.stop_service, foreground="red")
        self.add_command(label="打开配置文件", command=self.open_config)

    def start_service(self, *args, **kwargs):
        service_status = FrpUtils().check_service()
        if service_status:
            TextPopup(self.root).add_text("服务正在运行")
        FrpUtils().start_service()
        TextPopup(self.root).add_text("服务已启动")
        StopEvents().add("Frp", FrpUtils().stop_service)

    def stop_service(self, *args, **kwargs):
        FrpUtils().stop_service()
        TextPopup(self.root).add_text("服务已关闭")
        StopEvents().remove("Frp")

    def open_config(self, *args, **kwargs):
        FrpUtils().open_config()

    def check_service(self, is_popup=True, **kwargs):
        status = False
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] == config.frpc.name:
                status = True
                break
        if is_popup:
            TextPopup(self.root).add_text("未运行" if not status else "服务正在运行")
        return status

    def onLeftClick(self, event):
        self.unpost()


class SSHMenu(BaseMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        data = SshUtils().load_data()
        for info in data:
            self.add_command(label=info["text"], command=self.ssh(info["details"]))

    def ssh(self, conf):
        def wrapper():
            SshUtils().ssh(conf)

        return wrapper


class ScpMenu(BaseMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_command(label="打开", command=self.start_service)

    def start_service(self):
        from apps.scp.myscp import Main
        Main().run()


class LinkMenu(BaseMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for group, links in config.mylinks:
            self.add_command(label=group, font="Helvetica 10", state="disabled")
            for link in links:
                if not link.enable:
                    continue
                foreground = "black" if not link.foreground else link.foreground
                self.add_command(
                    label=link.name,
                    command=self.open_web(link.link),
                    foreground=foreground,
                )

            self.add_separator()

    def open_web(self, url):
        import webbrowser

        def wrapper():
            webbrowser.open(url)

        return wrapper


class HTTPMenu(BaseMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_command(label="检测", command=self.check_service)
        self.add_command(label="打开", command=self.start_service)
        self.add_command(label="关闭", command=self.stop_service)

        self.show_time = 10000

    def check_service(self, *args, **kwargs):
        if MyHttpUtil().check_service(config.http.port):
            TextPopup(self.root, self.show_time).add_text(
                f"服务正在运行:\n本地地址 {config.http.local_url}\n服务器地址 {config.http.url}"
            )
        else:
            TextPopup(self.root, self.show_time).add_text("服务未运行")

    def start_service(self, *args, **kwargs):
        try:
            MyHttpUtil().start_service(
                (config.http.host, int(config.http.port)), config.http.directory,True
            )
            TextPopup(self.root, self.show_time).add_text(
                f"服务已启动:\n本地地址 {config.http.local_url}\n服务器地址 {config.http.url}"
            )

        except Exception as e:
            TextPopup(self.root, self.show_time).add_text(str(e))

    def stop_service(self, *args, **kwargs):
        try:
            MyHttpUtil().stop_service(config.http.port)
            TextPopup(self.root, self.show_time).add_text("服务已停止")
        except Exception as e:
            TextPopup(self.root, self.show_time).add_text(str(e))


class PetMenu(BaseMenu):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_cascade(label="frp", menu=FrpMenu(main=self))
        self.add_cascade(label="Ssh", menu=SSHMenu(main=self))
        self.add_cascade(label="Scp", menu=ScpMenu(main=self))
        self.add_cascade(label="HttpServer", menu=HTTPMenu(main=self))
        self.add_cascade(label="我的地址", menu=LinkMenu(main=self))

        self.add_separator()
        self.add_command(label="Quit", command=self.close)
        PetLogger.info("Pet APP:Init menu success!")

    def onLeftClick(self, event):
        self.unpost()
        if self.active:
            self.unpost()

    def onRightClick(self, event):
        self.unpost()
        self.post(event.x_root, event.y_root - self.winfo_height() - 30)
        self.active = True  # 设置菜单状态为活动
        self.lift()

    def open_config_file(self, *args, **kwargs):
        self.unpost()
        open_config_file()

    def open_ssh_config_file(self, *args, **kwargs):
        self.unpost()
        subprocess.Popen(["cmd", "/c", "start", "", config.ssh.commands], shell=True)

    def close(self, *args, **kwargs):
        self.unpost()
        self.main.quit()


class BiuPetMenu(PetMenu):
    def __init__(self, main: BasePetMaster, action, *args, **kwargs) -> None:
        super().__init__(main, *args, **kwargs)
        self.add_separator()
        self.add_command(label="喂食", command=self.eat_foot)
        self.add_command(label="玩耍", command=self.play)
        self.action = action

    def eat_foot(self, *args, **kwargs):
        self.unpost()
        self.action.eat_foot()

    def play(self, *args, **kwargs):
        self.unpost()
        self.action.play()

    def close(self, *args, **kwargs):
        self.unpost()
        self.action.close()
        self.after(2500, super().close)

class BallMenu(PetMenu):
    def __init__(self, main: BasePetMaster, action, *args, **kwargs) -> None:
        super().__init__(main, *args, **kwargs)
        self.add_separator()
        self.add_command(label="下一个", command=self.next_action)
        self.action = action

    def next_action(self, *args, **kwargs):
        self.action.change_image()
