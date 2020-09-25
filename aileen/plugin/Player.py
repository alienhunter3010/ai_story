from aileen.Feature import Feature
from aileen.Answer import Answer
from aileen.Handlers import Handlers

from pygame import mixer, error
import io


class Player(Feature):

    @staticmethod
    def play(source, arguments=None):
        mixer.music.load(io.BytesIO(source))
        mixer.music.play()

    def stop(self, trash, answer=Answer()):
        mixer.music.stop()
        return answer.append_rows(["STOP player"])

    def volume(self, arg, answer=Answer()):
        vol = mixer.music.get_volume()
        if arg == 'mute':
            vol = 0
        if arg == 'up':
            vol += 0.2
        elif arg == 'down':
            vol -= 0.2
        elif arg.startswith('+'):
            vol += (float(self.get_arguments(arg, '+')) / 100)
        elif arg.startswith('-'):
            vol -= (float(self.get_arguments(arg, '-')) / 100)
        elif arg.isnumeric():
            vol = float(arg) / 100
        mixer.music.set_volume(vol)
        return answer.append_rows([ "Volume is {}%".format(vol * 100) ])

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('stop', self.stop) \
            .add_control('volume', self.volume)

    def load(self, setup={}):
        try:
            mixer.init()
        except error:
            pass
