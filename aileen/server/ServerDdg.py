from aileen.Feature import Feature
from aileen.Answer import Answer
from aileen.Handlers import Handlers

import requests
import json


class ServerDdg(Feature):
    value = 5
    api_url = 'https://api.duckduckgo.com/?q={}&format=json'

    def search(self, what, question=None, answer=Answer()):
        r = requests.get(self.api_url.format(what))
        payload = json.loads(r.content)
        answer.style = 'ANSI'
        return answer.append_rows([
            payload['RelatedTopics'][0]['Text'] if payload['Abstract'] == '' else payload['Abstract']
        ])

    def greetings(self, trash, question=None, answer=Answer()):
        return answer.append_rows([
            "\t<code>Ddg</code> search engine is powered by <b>DuckDuckGo</b>'s API"
        ])

    def add_controls(self):
        Handlers.getInstance()\
            .add_control('search', self.search)\
            .add_control('greetings', self.greetings)
