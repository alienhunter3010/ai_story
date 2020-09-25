class Messages:
    def __init__(self):
        self.messages = []

    def add_all(self, msgs, last=False):
        self.messages.extend(msgs)
        if last:
            self.messages.append(False)

    def add(self, message, last=False):
        self.messages.append(message)
        if last:
            self.messages.append(False)

    def get_messages(self):
        return self.messages