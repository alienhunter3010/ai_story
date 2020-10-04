from aileen.Feature import Feature
from aileen.Answer import Answer
from aileen.Handlers import Handlers

import time
import requests
import json


class ServerUtils(Feature):
    value = 0

    def time(self, trash, question=None, answer=Answer()):
        return self.echo(time.strftime("Today is %Y-%m-%d, the time is %H:%M:%S"), answer)

    def ip(self, trash, question=None, answer=Answer()):
        r = requests.get("https://httpbin.org/ip")
        result = json.loads(r.text)
        return self.echo("On the Net I'm using {}".format(result["origin"]), answer)

    def real_ai(self, trash, question=None, answer=Answer()):
        return self.echo(
            "I'm not. This is just a game. Or maybe... I'm the seed of a new type of AI",
            answer
        )

    def where(self, trash, question=None, answer=Answer()):
        return self.echo("The answer is... from the Internet!", answer)

    def greetings(self, trash, question=None, answer=Answer()):
        return self.echo(
            "\t<code>Utils</code> plugin use some net functions from <b>httpbin.org</b> by Kenneth Reitz",
            answer
        )

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('what time is it', self.time) \
            .add_control('what is your ip', self.ip) \
            .add_control('are you a real ai', self.real_ai) \
            .add_control('where are you from', self.where) \
            .add_control('greetings', self.greetings) \
            .add_control('debug', self.echo)
