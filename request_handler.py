
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import argparse
from db_handler import DB_Handler


class S(BaseHTTPRequestHandler):

    db_handler = DB_Handler()

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers",
                         "X-Requested-With, Content-Type")
        self.end_headers()
        self.mode = "Access"

    def do_GET(self):
        try:
            # print(self.path)
            if self.path == '/api/getdata':
                self._set_headers()
                res = S.db_handler.get_access_keys()
                self.wfile.write(res.encode("utf8"))

            if "/api/getlog?id" in self.path:
                self._set_headers()
                key = str(self.path.split("=")[-1])
                # print(key)
                res = S.db_handler.get_last_access_time(key)
                if res:
                    # print(res)
                    self.wfile.write(res.encode("utf8"))
                else:
                    self.wfile.write("No Data Available".encode("utf8"))

            if self.path == '/api/getlogs':
                self._set_headers()
                self.wfile.write(S.db_handler.get_logs().encode("utf-8"))

            if self.path == '/api/getmode':
                self._set_headers()
                self.wfile.write(S.db_handler.get_mode().encode("utf-8"))

            if "/api/delete?id" in self.path:
                self._set_headers()
                key = str(self.path.split("=")[-1])
                S.db_handler.delete_data(key)
                self.wfile.write("ok".encode("utf8"))

        except Exception:
            self.wfile.write("error".encode("utf8"))
            raise Exception

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        try:
            if self.path == '/api/changemode':
                self._set_headers()
                content_len = int(self.headers.get('content-length', 0))
                post_body = json.loads(self.rfile.read(
                    content_len).decode('utf8').replace("'", '"'))
                print(post_body)
                with open('mode.txt', 'w') as f:
                    self.mode = post_body["mode"]
                    f.write(self.mode)
                self.wfile.write("ok".encode("utf8"))

            if "/api/changename?id" in self.path:
                self._set_headers()
                key = str(self.path.split("=")[-1])
                name = json.loads(self.rfile.read(
                    int(self.headers.get('content-length', 0))).decode('utf8').replace("'", '"'))["name"]

                S.db_handler.change_name(name, key)

                print(key, name)
                self.wfile.write("ok".encode("utf8"))

            if "/api/adddata?id" in self.path:
                self._set_headers()
                key = str(self.path.split("=")[-1])
                name = json.loads(self.rfile.read(
                    int(self.headers.get('content-length', 0))).decode('utf8').replace("'", '"'))["name"]

                print(key, name)
                S.db_handler.add_access_key_and_name(name, key)

                self.wfile.write("ok".encode("utf8"))

        except Exception:
            self.wfile.write("error".encode("utf8"))
            raise Exception

    def do_OPTIONS(self):
        self._set_headers()


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print("Starting httpd server on {}:{}".format(addr, port))
    httpd.serve_forever()


def run_server_process():

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
