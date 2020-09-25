from aileen.Feature import Feature
from aileen.Handlers import Handlers
from aileen.Answer import Answer


class ServerSetup(Feature):

    def help(self, trash, answer=Answer()):
        return answer.append_rows([
            "\n  <bold>Setup commands:</bold>",
            "\t<pre>add (feature)</pre>\tadd a new ability"
        ])

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('help', self.help)
