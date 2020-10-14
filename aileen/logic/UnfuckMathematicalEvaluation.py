from chatterbot.logic import MathematicalEvaluation

class UnfuckMathematicalEvaluation(MathematicalEvaluation):
    def process(self, input_statement, additional_response_selection_parameters=None):
        stm = super().process(input_statement, additional_response_selection_parameters)
        parts = stm.text.split(' = ')
        if len(parts) == 2 and parts[0] == parts[1]:
            stm.confidence = 0
        return stm
