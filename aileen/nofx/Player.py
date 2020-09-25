from aileen.Binary import Typed


class Player(Typed):

    @staticmethod
    def play(source, arguments=None):
        return Typed.to_dict(source, 'audio')
