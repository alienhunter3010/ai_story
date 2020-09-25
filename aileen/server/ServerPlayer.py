from aileen.Binary import Binary
from aileen.Handlers import Handlers
from aileen.Answer import Answer

import requests


class ServerPlayer(Binary):
    computoser_url = 'http://computoser.com/music/get?mood=MAJOR&tempo=MEDIUM&accompaniment=OPTIONAL&instrument=-1&scale=&classical=false&electronic=NO&drums=OPTIONAL&preferDissonance=false'
    computoser_mp3 = 'http://dhvexktaalgrs.cloudfront.net/{}.mp3'
    value = 10

    def __init__(self):
        super().__init__(['aileen.{}.Player', 'Player', 'play'])

    def add_controls(self):
        h = Handlers.getInstance()\
            .add_control('play', self.play) \
            .add_control('compose', self.compose) \
            .add_control('greetings', self.greetings)

    def compose(self, trash, answer=Answer()):
        r = requests.get(self.computoser_url)
        response = requests.get(self.computoser_mp3.format(r.text))
        if response.content is None:
            return answer.append_rows("Unable do compose new music, actually")
        else:
            answer.binary = response.content
            answer.append_rows(["Let's play {}'s song".format(r.text)])
            # Cache it
            fn = "assets/music/{}.mp3".format(t.text)
            with open(fn, 'wb') as fp:
                fp.write(answer.binary)
            return self.play(r.text, answer=answer)

    def play(self, cached_song, answer=Answer()):
        try:
            if answer.binary is None:
                if cached_song is not None:
                    fn = "assets/music/{}.mp3".format(cached_song)
                    with open(fn, 'rb') as fp:
                        answer.binary = fp.read()
                else:
                    answer.append_rows(["Sorry, I have nothing to play"])
                    return answer
            answer.setup['parser'] = self.parser
            answer.setup['arguments'] = cached_song
        except FileNotFoundError:
            answer.append_rows(["Sorry, file '{}' not found".format(fn)])
        return answer

    def greetings(self, trash, answer=Answer()):
        return answer.append_rows([
            "\t<code>Player</code> plugin load self-generated music from <b>computoser.com</b> by Bozhidar Bozhanov"
        ])
