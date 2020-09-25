class Persist:

    def get_first(self, a, b):
        return b if a is None else a

    def load(self, setup):
        pass

    def save(self, exiting=False):
        return {}
