import json
import logging

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

from aileen.Answer import Answer
from aileen.Feature import Feature


class Injectable:

    def inject_adapter(self, bot, class_adapter):
        adapter = class_adapter(bot)
        try:
            bot.logic_adapters.append(adapter)
        except FileNotFoundError:
            logging.warning("{} adapter w/o train".format(adapter))
        return self


class PluggableAdapters(Feature, Injectable):
    chattable = True

    def __init__(self, bot=None, setup=None, **kwargs):
        Feature.__init__(self, setup=setup)
        self.register_adapters(bot, **kwargs)
        self.corpus = None
        self.list = None

    def train(self, bot):
        if self.corpus is not None:
            trainer = ChatterBotCorpusTrainer(bot)
            trainer.train(self.corpus)
        elif self.list is not None:
            trainer = ListTrainer(bot)
            trainer.train(self.list)

    # Override me
    def register_adapters(self, bot, **kwargs):
        pass


class AutoAdapter(LogicAdapter, Injectable):
    chattable = True

    # You can use this class as a stand alone plugin, or stack it into a PluggableAdapter
    def __init__(self, bot=None, setup=None, **kwargs):
        LogicAdapter.__init__(self, bot, **kwargs)

    # Override me
    def process(self, input_statement, additional_response_selection_parameters=None):
        result = Statement(text=None)
        result.confidence = 0
        return result


class Chatter:

    def __init__(self):
        # Create a basic instance of a ChatBot.
        # Additional adapter will be injected from Cluster
        # training data will be added from Cluster
        self.bot = ChatBot(
            'AIleen',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=[
                'aileen.logic.UnfuckMathematicalEvaluation.UnfuckMathematicalEvaluation',
                {
                    'import_path': 'aileen.logic.WeakTimeLogicAdapter.WeakTimeLogicAdapter',
                    'negative': [
                        'who are you?',
                        'it is time to go to sleep',
                        'what is your favorite color',
                        'i had a great time',
                        'thyme is my favorite herb',
                        'do you have time to look at my essay',
                        'how do you have the time to do all this'
                        'what is it'
                    ]
                },
                'chatterbot.logic.BestMatch',
                'aileen.logic.UnknownLogicAdapter.UnknownLogicAdapter'
            ],
            database_uri='sqlite:///var/database.db',
            preprocessors=[
                'aileen.Chatter.to_lower'
            ]
        )

    def exec_control(self, command):
        answer = Answer()
        #try:
        bot_response = self.bot.get_response(command)
        #except TypeError:
        #    return answer
        try:
            return answer.merge_answer(json.loads(bot_response.text))
        except json.JSONDecodeError:
            return answer.append_rows([
                bot_response.text
            ])


def to_lower(statement):
    statement.text = statement.text.lower()
    return statement
