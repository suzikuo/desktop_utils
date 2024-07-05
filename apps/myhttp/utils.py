
from kernel.common import is_port_in_use, kill_process_using_port
from kernel.events import StopEvents
from log import MyLogger
from singleton import singleton


@singleton
class MyHttpUtil:
    def __init__(self) -> None:
        self.http_instance = None
        self.http = {}

    def check_service(self, port):
        if is_port_in_use(port):
            return True
        return False

    def save_address(self, address):

        if address:
            self.http = {"address": [address[0], address[1]]}
        else:
            self.http = {}

    def start_service(self, address, directory,https=False):
        from apps.myhttp.httpProcess import MyHttpProcess

        if is_port_in_use(address[1]):
            address = self.http.get("address", [])
            if address:
                return address

            error_message = f"端口{address[1]}被占用"
            MyLogger.error("Start Http Errpr:" + error_message)
            raise Exception(error_message)

        t = MyHttpProcess(address, directory,https)
        t.start()

        MyLogger.info(f"HTTP {address} Start!")
        self.save_address(address)

        StopEvents().add("MyHttpUtil", lambda: self._stop(address[1]))

        return address

    def stop_service(self, port=None, *args, **kwargs):

        if port:
            self._stop(port)
        StopEvents().remove("MyHttpUtil")

        self.save_address([])

        MyLogger.info("HTTP Shutdown!")

    def _stop(self, port=None):
        kill_process_using_port(port)


if __name__ == "__main__":
    MyHttpUtil().start_service(("", 6696), "C:\\Users\\98027\\Desktop",True)
