from aileen.Feature import Feature
from aileen.Answer import Answer
from aileen.Handlers import Handlers


class ServerCli(Feature):

    def __init__(self, setup=None):
        self.prompt = ' $ '
        self.has_history = False
        self.color_style = {}
        super().__init__(setup)

    def colors(self, trash=None, question=None, answer=Answer()):
        self.color_style = {
            'simple': '#000000 bg:ansigreen bold',
            'isimple': 'bg:#000000 ansigreen',
            'pre': 'ansigreen bold',
            'code': 'ansiyellow'
        }
        self.prompt = [
            ('class:simple', ' $ '),
            ('class:isimple', ' ')]

        answer.append_rows([ "Color support is <bold>on</bold>" ])
        answer.setup['local'] = ['aileen.{}.Cli', 'Cli', 'update_prompt']
        answer.setup['arguments'] = {
            'prompt': self.prompt,
            'style': self.color_style
        }
        return answer

    def whatsup(self, trash, question=None, answer=Answer()):
        answer.append_rows(["L<b>AI</b>fe is monochrome" if len(self.color_style) < 2 else "Feel enl<b>AI</b>ghted"])
        return answer

    def persist_history(self, trash=None, question=None, answer=Answer()):
        answer.append_rows(["History log is <bold>on</bold>"])
        answer.setup['history'] = self.has_history = True
        return answer

    def add_controls(self):
        h = Handlers.getInstance()
        h.add_control('add history', self.persist_history)
        h.add_control('add colors', self.colors)
        h.add_control('how do you do', self.whatsup)

    def load(self, source={}):
        if source.get('prompt'):
            self.prompt = source.get('prompt')
        if source.get('history') is True:
            self.has_history = True
        if source.get('style'):
            self.color_style = source.get('style')

    def save(self, exiting=False):
        return {
            'prompt': self.prompt,
            'style': self.color_style,
            'history': self.has_history
        }