from aileen.Answer import Answer
from aileen.Persist import Persist


class Feature(Persist):
    value = 0

    def control(self, cmd):
        return []

    def get_value(self):
        return self.value

    def get_arguments(self, cmd, drop):
        return cmd.replace(drop, '').strip()

    def add_controls(self):
        pass

    def echo(self, msg, answer=Answer()):
        return answer.append_rows([
            msg
        ])

    def get_pure_name(self):
        return Feature.get_pure_name_of(self.__class__)

    @staticmethod
    def get_pure_name_of(clazz):
        return clazz.__name__.replace('Server', '')