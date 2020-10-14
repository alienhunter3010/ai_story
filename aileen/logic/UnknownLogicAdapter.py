import random

from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class UnknownLogicAdapter(LogicAdapter):
    explain_phrases = [
        "Uhm... can you explain better?",
        "Antani and the superdicker with right entity.",
        "I'm not sure, give me more data, please.",
        "Can I ask you to explain with other words?",
        "I'm not able to answer.",
        "We run in circle. It's a Mad World."
    ]

    def can_process(self, statement):
        return True

    def process(self, input_statement, additional_response_selection_parameters=None):
        stm = Statement(random.choice(self.explain_phrases))
        stm.confidence = 0.1
        return stm
