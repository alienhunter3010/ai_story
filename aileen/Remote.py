import socket
import daemon
import time
import json

from aileen.IO import IO


class Remote:

    def __init__(self):
        self.soc = socket.socket()
        shost = socket.gethostname()
        ip = socket.gethostbyname(shost)
        self.server_host = shost # local
        self.port = 50000

    def connect(self):
        tries = 10
        while True:
            try:
                self.soc.connect((self.server_host, self.port))
                break
            except socket.timeout:
                from aileen import Mind

                IO.print("Where is my mind?\nTrying to start daemon")
                with daemon.DaemonContext():
                    o = Mind()
                    o.run()
                time.sleep(5)
            except ConnectionRefusedError:
                if tries > 0:
                    IO.print("Where is my mind?\nMaybe I can try again...")
                    time.sleep(10)
                    tries -= 1
                else:
                    IO.print('Sorry, exiting')
                    exit(1)

    def send_command(self, cmd):
        self.soc.send(cmd.encode())

    def receive_answer(self, buffer=4096):
        answer = self.receive_binary(buffer)
        return json.loads(answer.decode())

    def receive_binary(self, buffer=4096):
        return self.recvall(buffer)

    def solve(self, cmd):
        self.send_command(cmd)
        return self.receive_answer()

    def recvall(self, buffer=4096):
        data = b''
        while True:
            part = self.soc.recv(buffer)
            data += part
            if len(part) < buffer:
                # either 0 or end of data
                break
        return data


