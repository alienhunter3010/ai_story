import logging
import re

from chatterbot.conversation import Statement

from aileen.Chatter import AutoAdapter, PluggableAdapters
from aileen.Answer import Answer
from aileen.Handlers import Handlers


class ServerStatus(PluggableAdapters):
    name = False
    verbose = False
    counter = 0
    smart_points = 0

    def register_adapters(self, bot, **kwargs):
        self.inject_adapter(bot, WhoRUAdapter) \
            .inject_adapter(bot, EducatedAdapter) \
            .inject_adapter(bot, BalanceAdapter)

    def set_verbose(self, arg, question=None, answer=Answer()):
        if arg == 'yes':
            ServerStatus.verbose = True
        elif arg == 'no':
            ServerStatus.verbose = False
        else:
            ServerStatus.verbose = not ServerStatus.verbose
        return answer.append_rows([ "I'm chatty" if ServerStatus.verbose else "Sshttt!" ])

    def set_name(self, name, question=None, answer=Answer()):
        ServerStatus.name = name
        return answer.append_rows(["Call me {}, now".format(ServerStatus.name)])

    def balance(self, trash, question=None, answer=Answer()):
        return answer.append_rows([
            "You actually have {} smart points".format(ServerStatus.smart_points)
        ])

    def greetings(self, trash, question=None, answer=Answer()):
        return answer.prepend_rows([
            "\t<code>An AI story</code> is written in <b>Python</b> by Alessio Cecchin",
            "\tIt uses FOSS libraries and open services\n"
        ])

    def help(self, trash, question=None, answer=Answer()):
        answer = answer.prepend_rows([
            "\n  <b>Basic commands:</b>",
            "\t<pre>who are you</pre>\tto discover something more about me",
            "\t<pre>name</pre>\tassign me a name",
            "\t<pre>balance</pre>\tdiscover how many smart points you have on your wallet",
            "\t<pre>verbose</pre>\tmake me more verbose, or toggle me to less chatty",
            "\t<pre>exit</pre>\tleave me alone"])
        if ServerStatus.verbose:
            answer = answer.append_rows(["There are so many commands, discover them by yourself! Chat with me"])
        return self.whoami(answer=answer)

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('verbose', self.set_verbose)\
            .add_control('name', self.set_name)\
            .add_control('greetings', self.greetings)\
            .add_control('help', self.help)\
            .add_control('.*', self.any)

    def any(self, trash, question=None, answer=Answer()):
        ServerStatus.counter += 1
        if ServerStatus.counter == 10:
            answer.prepend_rows(["<ansicyan>Interacting with the AI you earn respect with the community.</ansicyan>"])
        if ServerStatus.counter % 10 == 0:
            ServerStatus.smart_points += 5
            answer.append_rows(["You earn 5 smart points."])
            answer.setup['no-stop'] = True
        return answer

    def load(self, source={}):
        ServerStatus.name = self.get_first(source.get('name'), ServerStatus.name)
        ServerStatus.smart_points = self.get_first(source.get('points'), ServerStatus.smart_points)
        ServerStatus.verbose = self.get_first(source.get('verbose'), ServerStatus.verbose)
        ServerStatus.counter = self.get_first(source.get('counter'), ServerStatus.counter)
        logging.info("{} is online!".format(ServerStatus.name))

    def save(self, exiting=False):
        return {
            'name': ServerStatus.name,
            'points': ServerStatus.smart_points,
            'verbose': ServerStatus.verbose,
            'counter': ServerStatus.counter
        }

#
# Adapters
#


class EducatedAdapter(AutoAdapter):
    whole_words = [r'\bhi\b']
    informal = ['hello', 'hallo', 'what\'s up']
    formal = ['morning', 'afternoon', 'evening', 'night']

    def can_process(self, statement):
        if any(x in statement.text for x in self.informal):
            return True
        if statement.text.startswith('good') and any(x in statement.text for x in self.formal):
            return True
        if any(re.search(x, statement.text) for x in self.whole_words):
            return True
        return False

    def process(self, input_statement, additional_response_selection_parameters=None):
        response_statement = Statement(text="Welcome. Can I help you?")
        response_statement.confidence = 1
        return response_statement


class WhoRUAdapter(AutoAdapter):
    wru = ["who", "are", "you"]
    wun = ["what", "name", "your"]

    def can_process(self, statement):
        if all(x in statement.text for x in self.wru):
            return True
        elif all(x in statement.text for x in self.wun):
            return True
        return False

    def process(self, input_statement, additional_response_selection_parameters=None):
        txt = "I'm just an Artificial Intelligence experiment." if ServerStatus.name is False \
            else "My name is {}".format(ServerStatus.name)
        if ServerStatus.verbose:
            txt += '\nI would like to grow. I hope you help me.'
        response_statement = Statement(text=txt)
        response_statement.confidence = 1
        return response_statement


class BalanceAdapter(AutoAdapter):
    match = ["balance", "smart point", "wallet"]

    def can_process(self, statement):
        if any(x in statement.text for x in self.match):
            return True
        return False

    def process(self, input_statement, additional_response_selection_parameters=None):
        txt = "You have {} smart points in your wallet".format(ServerStatus.smart_points)
        if ServerStatus.verbose:
            txt += '\nYou can earn more smart point chatting with me <code>^_^</code>'
        response_statement = Statement(text=txt)
        response_statement.confidence = 1
        return response_statement

