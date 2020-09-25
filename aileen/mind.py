
from aileen.IO import IO

from aileen.Cluster import ServerCluster
from aileen.Handlers import Handlers

import socket
import threading
import json
import time
import signal
import logging


class Mind:

    def __init__(self):
        self.client_connections = []
        self.cluster = ServerCluster()
        self.socket = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 50000                # Reserve a port for your service.
        self.pill2kill = threading.Event()
        signal.signal(signal.SIGTERM, self.sig_heil)
        signal.signal(signal.SIGINT, self.sig_heil)

        while True:
            try:
                self.socket.bind((host, port))        # Bind to the port
                logging.info("Listening on {}:{}".format(host, port))
                break;
            except OSError:
                logging.info("Address in use. Trying again in 10 secs")
                time.sleep(10)

    def sig_heil(self, signal, frame):
        logging.info('SIG({}) received'.format(signal))
        self.clean_exit()

    def run(self):
        self.socket.listen(5)                  # Now wait for client connection.
        while True:
            c, addr = self.socket.accept()     # Establish connection with client.
            #c.settimeout(2)
            t = threading.Thread(target=self.dialog, args=(c, addr, self.pill2kill))
            t.start()
            self.client_connections.append(t)
        self.clean_exit()

    def clean_exit(self):
        self.cluster.save_evolution(exiting=True)
        self.socket.close()
        self.pill2kill.set()
        for thread in self.client_connections:
            if thread.is_alive():
                try:
                    thread.join()
                except RuntimeError:
                    pass
        logging.info('\nBye bye')
        exit(0)

    def dialog(self, clientsocket, address, stop_event):
        clientsocket.send(
            self.pack(self.cluster.get_evolution(client=True)).encode()
        )
        while True:
            try:
                cmd = clientsocket.recv(1024).decode()
            except socket.timeout:
                continue
            if cmd == 'gOOd-bYe':
                break
            elif cmd.startswith('shUt-dOwn'):
                clientsocket.close()
                self.clean_exit()
            answer = Handlers.getInstance().exec_control(cmd)
            clientsocket.send(self.pack(answer.get_dict()).encode())
            if answer.binary is not None:
                time.sleep(0.1)
                clientsocket.send(answer.binary)
        clientsocket.close()

    def pack(self, messages):
        return json.dumps(messages)

# Use `python3 -m aileen mind` to launch this as daemon