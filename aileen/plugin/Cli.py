from prompt_toolkit.document import Document

from aileen.AIIO import AIIO
from aileen.IO import IO
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import PathCompleter, Completer, Completion

from aileen.intersect.Arguments import WithFS


class ConditionedPathCompleter(Completer):

    def __init__(self):
        self.path_completer = PathCompleter()

    def get_completions(self, document, complete_event):
        for cmd in WithFS.commands:
            if WithFS.here(cmd):
                sub_doc = Document(document.text.replace(cmd, '').strip())
                yield from (Completion(completion.text, completion.start_position, display=completion.display)
                            for completion
                            in self.path_completer.get_completions(sub_doc, complete_event))


class Cli(AIIO):
    prompt = ' $ '
    session = PromptSession(completer=ConditionedPathCompleter())
    has_history = False
    style_dict = {}

    def __init__(self):
        super().__init__()

    def ask(self, message=False):
        return self.session.prompt(
            self.prompt if message is False else '{} '.format(message),
            style=IO.style
        )

    @staticmethod
    def update_style(dict):
        Cli.style_dict = dict
        IO.style = Style.from_dict(Cli.style_dict)

    @staticmethod
    def update_prompt(arguments):
        Cli.prompt = arguments['prompt']
        Cli.update_style(arguments['style'])

    def talk(self, message, style=None):
        if style == 'ANSI':
            IO.printANSI(message)
        else:
            IO.print(message)

    def persist_history(self, trash=None):
        Cli.session = PromptSession(history=FileHistory('var/history.txt'),
            completer=ConditionedPathCompleter())

    def load(self, source={}):
        if source.get('prompt'):
            Cli.prompt = source.get('prompt')
        if source.get('history') is True:
            self.persist_history()
        if source.get('style'):
            self.update_style(source.get('style'))

