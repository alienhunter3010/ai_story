from aileen.Answer import Answer
from aileen.Feature import Feature
from aileen.Handlers import Handlers

from pyquery import PyQuery


class ServerDoomsday(Feature):
    value = 5

    def clock(self, trash, question=None, answer=Answer()):
        d = PyQuery("https://thebulletin.org/doomsday-clock/current-time/")
        p = d('h2')
        # TODO: sanificare meglio
        return self.echo(p.html().replace('<br/>', '\n'), answer)

    def greetings(self, trash, question=None, answer=Answer()):
        return self.echo(
            "\tThe <code>Doomsday Clock</code> is here <b>thebulletin.org</b> we parse the current time's page with PyQuery",
            answer
        )

    def add_controls(self):
        Handlers.getInstance() \
            .add_control('minutes to midnight', self.clock) \
            .add_control('greetings', self.greetings)