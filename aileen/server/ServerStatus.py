from aileen.Feature import Feature
from aileen.Answer import Answer
from aileen.Handlers import Handlers


class ServerStatus(Feature):
    name = False
    verbose = False
    counter = 0
    smart_points = 0

    def set_verbose(self, arg, question=None, answer=Answer()):
        if arg == 'yes':
            self.verbose = True
        elif arg == 'no':
            self.verbose = False
        else:
            self.verbose = not self.verbose
        return answer.append_rows([ "I'm chatty" if self.verbose else "Sshttt!" ])

    def set_name(self, name, question=None, answer=Answer()):
        self.name = name
        return answer.append_rows(["Call me {}, now".format(self.name)])

    def balance(self, trash, question=None, answer=Answer()):
        return answer.append_rows([
            "You actually have {} smart points".format(self.smart_points)
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
        if self.verbose:
            answer = answer.append_rows(["There are so many commands, discover them by yourself! Chat with me"])
        return self.whoami(answer=answer)

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('verbose', self.set_verbose)\
            .add_control('name', self.set_name)\
            .add_control('who are you', self.whoami)\
            .add_control('balance', self.balance)\
            .add_control('greetings', self.greetings)\
            .add_control('help', self.help)\
            .add_control('.*', self.any)

    def any(self, trash, question=None, answer=Answer()):
        self.counter += 1
        if self.counter == 10:
            answer.prepend_rows(["<ansicyan>Interacting with the AI you earn respect with the community.</ansicyan>"])
        if self.counter % 10 == 0:
            self.smart_points += 5
            answer.append_rows(["You earn 5 smart points."])
        return answer

    def whoami(self, trash=None, question=None, answer=Answer()):
        if self.verbose:
            answer.append_rows(['I would like to grow. I hope you help me.'])
        return answer.prepend_rows(['\nI am an AI.' if self.name is False else "\nMy name is {}".format(self.name)])

    def load(self, source={}):
        self.name = self.get_first(source.get('name'), self.name)
        self.smart_points = self.get_first(source.get('points'), self.smart_points)
        self.verbose = self.get_first(source.get('verbose'), self.verbose)
        self.counter = self.get_first(source.get('counter'), self.counter)

    def save(self, exiting=False):
        return {
            'name': self.name,
            'points': self.smart_points,
            'verbose': self.verbose,
            'counter': self.counter
        }
