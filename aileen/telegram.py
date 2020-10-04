from aileen.Callbackable import Callbackable
from aileen.Remote import Remote
from aileen.Cluster import NoFxCluster
from aileen.Handlers import Handlers
from aileen.plugin import *

from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters

import re
import time

from aileen.Config import Keys


class Telegram(Remote):
    updater = None
    token = '123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ012345678'
    cmds = []

    def __init__(self):
        Keys.load()
        key = Keys.get('Telegram')
        Telegram.token = key['token']

        self.cluster = NoFxCluster()
        super().__init__()

    def check_token(self):
        return re.match('[0-9]{9}:.{35}', self.token)

    def set_token(self, token):
        Telegram.token = token
        if not self.check_token():
            print("FATAL: Invalid token. Ask to Botfather")
            exit(1)

    def ask(self, message=False):
        if not self.check_token():
            print("FATAL: Invalid token. Ask to Botfather")
            exit(1)
        self.listen()

    def listen(self):
        Telegram.updater = Updater(Telegram.token)
        dp = Telegram.updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text, self.deliver))
        Telegram.updater.start_polling()
        Telegram.updater.idle()

    def run(self):
        self.connect()
        self.cluster.load_config(
            self.receive_answer()
        )
        while True:
            self.ask()

    def deliver(self, bot, update):
        chat_id = update.message.chat_id
        answer = Handlers.getInstance().exec_control(update.message.text)
        if not answer.has_totalk():
            answer = self.solve(update.message.text)
        self.output(bot, chat_id, answer)

    def output(self, bot, chat_id, answer):
        for row in answer['rows']:
            bot.send_message(chat_id, row, parse_mode='html' if answer['style'] == 'HTML' else None)
            time.sleep(1)
        for row in answer['raw_rows']:
            bot.send_message(chat_id, row)
            time.sleep(1)
        if 'parser' in answer['setup']:
            what_is = Callbackable.solve_callback(answer['setup']['parser'], self.cluster)(self.receive_binary(), arguments=Callbackable.optional(answer['setup'], 'arguments', None))
            if what_is['type'] == 'image':
                bot.send_photo(chat_id, what_is['payload'])
            elif what_is['type'] == 'audio':
                bot.send_audio(chat_id, what_is['payload'])

# Use `python3 -m aileen telegram` to launch this client