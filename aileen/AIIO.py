from aileen.Feature import Feature


class AIIO:

    def __init__(self):
        super().__init__()

    def ask(self):
        pass

    def talk(self, message, style=None):
        print(message)

    def chat(self, messages):
        for message in messages:
            if isinstance(message, tuple):
                self.talk(message[0], message[1])
            else:
                self.talk(message)
