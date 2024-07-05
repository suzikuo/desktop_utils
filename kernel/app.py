from apps.pets.app import PetsApp

from singleton import singleton


@singleton
class MyApp:
    def __init__(self) -> None:
        self._stopping = False

    def run(self):
        # 启动托盘图标
        # IconMenu().run()
        # 启动app
        PetsApp().run()

        self.stop()


    def stop(self):
        # 停止托盘图标
        # IconMenu().exit_app()

        if self._stopping:
            return
        self._stopping = True
        from kernel.events import StopEvents

        stop_events = StopEvents()
        for name, event in stop_events.l.items():
            stop_events.stop(name, event)

        self._stopping = False


if __name__ == "__main__":
    MyApp().run()
