import logging

from aileen.Answer import Answer
from aileen.Chatter import AutoAdapter, PluggableAdapters

import requests
import json


class ServerUtils(PluggableAdapters):
    value = 0

    def __init__(self, bot=None, setup=None, **kwargs):
        super().__init__(bot=bot, setup=setup, **kwargs)
        # Load all and now
        self.corpus = './var/corpus'
        self.train(bot)

    def register_adapters(self, bot, **kwargs):
        self.inject_adapter(bot, ipAdapter)

    def greetings(self, trash, question=None, answer=Answer()):
        return self.echo(
            "\t<code>Utils</code> plugin use some net functions from <b>httpbin.org</b> by Kenneth Reitz",
            answer
        )

#
# Adapters
#


class ipAdapter(AutoAdapter):

    def can_process(self, statement):
        if statement.text.startswith('what is your ip'):
            return True
        return False

    def ip(self):
        r = requests.get("https://httpbin.org/ip")
        result = json.loads(r.text)
        return "On the Net I'm using {}".format(result["origin"])

    def process(self, input_statement, additional_response_selection_parameters=None):
        result = super().process(input_statement, additional_response_selection_parameters)
        if input_statement.text.startswith('what is your ip'):
            result.text = self.ip()
            result.confidence = 1
        return result