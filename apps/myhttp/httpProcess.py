import multiprocessing
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any


from log import MyLogger


class MyHandler:
    def __init__(self, directory) -> None:
        self.directory = directory

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        _directory = self.directory
        try:
            class MyHttpHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, directory=None,**kwargs):
                    
                    super().__init__(*args, directory=_directory, **kwargs)

            return MyHttpHandler(*args, **kwds)
        except Exception as e:
            MyLogger.info("Handler call error:{}".format(e))
            return SimpleHTTPRequestHandler


class MyhttpServer(HTTPServer):
    def __init__(self,address, directory,*args,**kwargs) -> None:
        super().__init__(address, MyHandler(directory),*args,**kwargs)

    def start(self):
        self.serve_forever()

class MyhttpsServer():
    def __init__(self,address, directory,*args,**kwargs) -> None:
        self.cert = self.load_cert()
        self.address = address
        self.bind = address[0]
        self.port = address[1]
        self.directory = directory
    
    def load_cert(self):
        import os
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/privateKey.pem'
        return file_path
    
    def start(self):
        from https.server import ThreadingHTTPSServer, partial

        handler_class = partial(MyHandler(self.directory), directory=self.directory)
        handler_class.protocol_version = "HTTP/1.1"

        with ThreadingHTTPSServer(self.cert, self.address, handler_class) as httpd:
            httpd.socket.getsockname()
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting.")

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


class MyHttpProcess(multiprocessing.Process):
    def __init__(self, address, directory, https=False,*args, **kwargs) -> None:
        super().__init__(name="MyHttpProcess")
        self.address, self.directory = address, directory
        self.https = https

    def run(self) -> None:
        if self.https:
            MyhttpsServer(self.address, self.directory).start()
        else:
            MyhttpServer(self.address, self.directory).start()
        
