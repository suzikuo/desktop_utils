from log import MyLogger
from singleton import singleton


@singleton
class StopEvents:
    def __init__(self) -> None:
        self.l = {}

        self._all_closes = []

    def add(self, key, event):
        self.l[key] = event
        if key in self._all_closes:
            self._all_closes.remove(key)

    def remove(self, key):
        if key not in self.l:
            return
        del self.l[key] 
        if key in self._all_closes:
            self._all_closes.remove(key)

    def stop(self,key,event):
        if key in self._all_closes:
            return
        try:
            event() 
            self._all_closes.append(key)
        except Exception as e:
            MyLogger.error(f"[StopEvents.stop] {key} stop error:{e}")

        