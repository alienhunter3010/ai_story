from aileen.Binary import Binary

from aileen.Handlers import Handlers
from aileen.Answer import Answer


class ServerViewer(Binary):
    value = 10

    def __init__(self):
        super().__init__(['aileen.{}.Viewer', 'Viewer', 'view'])

    def add_controls(self):
        h = Handlers.getInstance()\
            .add_control('view', self.view)\
            .add_control('greetings', self.greetings)

    def view(self, source, answer=Answer()):
        return self.binary(source, answer)

    def greetings(self, trash, answer=Answer()):
        return answer.append_rows([
            "\t<code>Viewer</code> plugin is inspired to <b>viu</b> written in Rust by Atanas Yankov"
        ])