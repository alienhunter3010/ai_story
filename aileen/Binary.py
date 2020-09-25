import urllib.request
from io import BytesIO
from urllib.error import URLError

from aileen.Answer import Answer
from aileen.Feature import Feature


class Binary(Feature):

    def __init__(self, parser=[]):
        self.parser = parser

    def load_binary(self, source, answer):
        if source.find('://') > 0:
            try:
                answer.binary = urllib.request.urlopen(source).read()
            except URLError:
                answer.append_rows(["URL not found {}".format(source)])
            return answer
        with open(source, 'rb') as fp:
            try:
                answer.binary = fp.read(-1)
            except FileNotFoundError:
                answer.append_rows(["File not found {}".format(source)])
        return answer

    def binary(self, source, answer=Answer()):
        answer = self.load_binary(source, answer)
        if answer.binary is not None:
            answer.setup['parser'] = self.parser
        return answer


class Typed(Feature):

    @staticmethod
    def to_dict(source, type):
        binary = BytesIO()
        binary.write(source)
        binary.seek(0)
        return {
            'payload': binary,
            'type': type
        }