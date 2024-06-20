import json
import threading
import time
from queue import Queue


from kernel.settings import config


def add_newline(text, chunk_size=15):
    result = ""
    for i in range(0, len(text), chunk_size):
        result += text[i : i + chunk_size] + "\n"
    return result


class HitokotoThread(threading.Thread):
    def __init__(self, queue: Queue, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.flag = True
        self.queue = queue
        self.ping_queue = Queue()
        self.text_index = 0
        self.ping_index = 0

    def run(self):
        import requests

        while self.flag:
            ping = self.get_ping()
            if ping:
                continue
            if self.text_index % 10 == 0:
                self.queue.put("")
            if self.text_index % 20 == 0:
                try:
                    response = requests.get(config.pet.hitokoto, timeout=3)
                    hitokoto = json.loads(response.text).get("hitokoto")
                except Exception:
                    pass
                self.queue.put(hitokoto)
                self.text_index = 0
            self.text_index += 1
            time.sleep(1)

    def stop(self):
        self.flag = False

    def get_ping(self):
        ping = None
        try:
            ping = self.ping_queue.get_nowait()
            self.ping_index = 0
            return ping
        except Exception:
            pass
        self.ping_index += 1
        if self.ping_index >= 3:
            self.stop()
        return None


class Hitokoto:
    """
    一言
    """

    def __init__(self, text_label):
        self.text_label = text_label
        self.text_index = 0
        self.queue = Queue()
        self.thread = HitokotoThread(self.queue)

    def start(self):
        self.thread.start()
        self.update_hitokoto()

    def update_hitokoto(self):
        if not self.queue.empty():
            hitokoto = self.queue.get()
            self.text_label.config(text=add_newline(hitokoto, 16))

        self.text_label.after(1000, self.update_hitokoto)

        if self.thread.ping_queue.empty():
            self.thread.ping_queue.put("ping")

    def set_text(self, text):
        self.text_label.config(text=add_newline(text, 16))

    def on_closing(self):
        self.thread.stop()

    def quit(self):
        self.thread.stop()
