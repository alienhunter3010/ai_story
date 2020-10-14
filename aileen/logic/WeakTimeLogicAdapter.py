from chatterbot.logic import TimeLogicAdapter

class WeakTimeLogicAdapter(TimeLogicAdapter):
    def process(self, input_statement, additional_response_selection_parameters=None):
        stm = super().process(input_statement, additional_response_selection_parameters)
        stm.confidence /= 2
        return stm
