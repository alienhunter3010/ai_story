from aileen.Answer import Answer
import re


class Handlers:

    __instance = None

    @staticmethod
    def getInstance():
        if Handlers.__instance == None:
            Handlers()
        return Handlers.__instance

    def __init__(self):
        if Handlers.__instance != None:
            raise Exception("Handlers class is singleton, use Handlser.getInstance() insteed")
        else:
            self.controls = {}
            Handlers.__instance = self

    def add_control(self, pattern, callback):
        if self.get_exact_control(pattern) is None:
            self.controls[pattern] = []
        self.controls[pattern].append(callback)
        return self

    def get_exact_control(self, pattern):
        return self.controls.get(pattern)

    def get_control(self, command):
        ctrl = {}
        for c in self.controls:
            if re.match(c, command):
                ctrl[c] = self.controls[c]
        return ctrl

    def exec_control(self, command):
        commands = self.get_control(command)
        answer = Answer()
        for c in commands:
            for m in commands[c]:
                answer = m(re.sub(c, '', command).strip(), question=command, answer=answer)
        return answer

