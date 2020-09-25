import os
import sys
import daemon
import logging


def mind():
    from aileen.mind import Mind

    logging.info("Inside Mind daemon!")
    o = Mind()
    o.run()


def telegram():
    from aileen.telegram import Telegram

    logging.info("Inside Telegram daemon!")
    o = Telegram()
    o.run()


def log_setup():
    logging.basicConfig(filename="/home/acecchin/projects/python/ai_story/var/aileen.log")


def daemonize(callback, working_directory="/"):
    with daemon.DaemonContext(working_directory=working_directory):
        callback()


logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
        level=logging.INFO)

if 'mind' in sys.argv:
    if 'fg' in sys.argv:
        mind()
    else:
        log_setup()
        daemonize(mind, working_directory=os.getcwd())
elif 'telegram' in sys.argv:
    if 'fg' in sys.argv:
        telegram()
    else:
        log_setup()
        daemonize(telegram)
else:
    from aileen.main import AIleen

    o = AIleen()
    o.run()
