import os
import sys
import daemon
import logging


class Main:

    def mind(self):
        from aileen.mind import Mind

        logging.info("Inside Mind daemon!")
        o = Mind()
        o.run()


    def telegram(self):
        from aileen.telegram import Telegram

        logging.info("Inside Telegram daemon!")
        o = Telegram()
        o.run()


    def log_setup(self):
        logging.info("Switching log to {}".format("{}/var/aileen.log".format(os.getcwd())))
        logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
            level=logging.INFO, filename="{}/var/aileen.log".format(os.getcwd()))


    def daemonize(self, callback, working_directory="/"):
        with daemon.DaemonContext(working_directory=working_directory):
            callback()

    def launcher(self, callback):
        if 'fg' in sys.argv:
            callback()
        else:
            self.log_setup()
            self.daemonize(callback, working_directory=os.getcwd())

    def start(self):
        logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                level=logging.INFO)

        if 'mind' in sys.argv:
            self.launcher(self.mind)
        elif 'telegram' in sys.argv:
            self.launcher(self.telegram)
        else:
            from aileen.main import AIleen

            o = AIleen()
            o.run()


app = Main()
app.start()
