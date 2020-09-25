from aileen.Binary import Typed


class Viewer(Typed):

    @staticmethod
    def view(source, arguments=None):
        return Typed.to_dict(source, 'image')