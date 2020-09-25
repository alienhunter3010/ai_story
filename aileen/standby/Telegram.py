from aileen.plugin.Cli import Cli
from aileen.Handlers import Handlers

from telegram.bot import Bot
from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters
import re
import os
import signal


# If Telegram is disabled or token is wrong, use the standard CLI interface
class Telegram(Cli):
    updater = None
    value = 50
    token = ''
    cli = True
    pid = -1
    enable = False
    cmds = []

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('token', self.set_token) \
            .add_control('disable telegram', self.off)\
            .add_control('enable telegram', self.on)

    def check_token(self):
        return re.match('[0-9]{9}:.{35}', self.token)

    def off(self, trash=None):
        Telegram.enable = False
        self.shutdown()

    def on(self, trash=None):
        Telegram.enable = True
        Telegram.pid = os.fork()
        if Telegram.pid > 0:
            # Main process make telegram bot running
            Telegram.cli = False
            self.listen()
        else:
            # Child process run the cli
            return [ "Now you can switch to Telegram, if you like" ]

    def set_token(self, token):
        Telegram.token = token
        if self.check_token():
            return ["Now I can talk with you on telegram!"]
        return ["Invalid token. Ask to Botfather"]

    def ask(self, message=False):
        if Telegram.cli or not Telegram.enable:
            return super().ask(message)
        if not self.check_token():
            self.talk("Invalid token. Ask to Botfather")
            return super().ask(message)
        self.listen()

    def listen(self):
        Telegram.updater = Updater(self.token)
        dp = Telegram.updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text, self.deliver))
        Telegram.updater.start_polling()
        signal.signal(signal.SIGTERM, self.shutdown)
        Telegram.updater.idle()

    def shutdown(self):
        if Telegram.pid > 0:
            print("Parent send signal...")
            os.kill(Telegram.pid, signal.SIGTERM)
        elif not Telegram.updater is None:
            print("...child receive signal")
            Telegram.updater.stop()

    def deliver(self, bot, update):
        chat_id = update.message.chat_id
        for msg in Handlers.getInstance().exec_control(update.message.text):
            if isinstance(msg, tuple):
                bot.send_message(chat_id, msg[0])
            else:
                bot.send_message(chat_id, msg, parse_mode='html')

    def load(self, source={}):
        self.set_token( self.get_first(source.get('token'), Telegram.token) )
        self.on() if self.get_first(source.get('enable'), Telegram.enable) else self.off()

    def save(self, exiting=False):
        if exiting:
            self.shutdown()
        return {
            'token': Telegram.token,
            'enable': Telegram.enable
        }
