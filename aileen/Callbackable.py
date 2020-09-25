import sys

from aileen.plugin import *
from aileen.nofx import *


class Callbackable:
    @staticmethod
    def optional(collection, key, default):
        return collection[key] if key in collection else default

    @staticmethod
    def solve_callback(signature, cluster):
        return getattr(
            getattr(sys.modules[signature[0].format(cluster.module)], signature[1]), signature[2]
        )
