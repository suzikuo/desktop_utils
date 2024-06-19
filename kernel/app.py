from apps.pets.app import PetsApp
from singleton import singleton
from .icon import IconMenu


@singleton
class MyApp:
    def run(self):
        # 启动托盘图标
        IconMenu().run()
        # 启动app
        PetsApp().run()

        self.stop()


    def stop(self):
        # 停止托盘图标
        IconMenu().exit_app()


if __name__ == "__main__":
    MyApp().run()
