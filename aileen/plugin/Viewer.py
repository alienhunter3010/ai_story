from aileen.Feature import Feature

import os
import io

from PIL import Image
from sty import fg, bg, rs

from aileen.intersect.Arguments import WithFS


class Viewer(Feature):
    two_pixels = '▄'

    def __init__(self, setup=None):
        WithFS.add_command('view')

    @staticmethod
    def view(source, arguments=None):
        img = Image.open(io.BytesIO(source))
        ox, oy = img.size
        rows, columns = os.popen('stty size', 'r').read().split()
        rows = int(rows) * 2
        columns = int(columns)
        if ox / columns < oy / rows:
            columns = int(ox * rows / oy)
        else:
            rows = int(columns * oy / ox)

        timg = img.resize((columns, rows), Image.BILINEAR)
        pixels = timg.load()  # create the pixel map

        for j in range(0, timg.size[1], 2):  # for every pixel:
            for i in range(0, timg.size[0]):
                Viewer.paint_two_pixels(pixels[i, j], pixels[i, j + 1])
            print("")
        return []

    @staticmethod
    def to_fg(pixel):
        return fg(pixel[0], pixel[1], pixel[2])

    @staticmethod
    def to_bg(pixel):
        return bg(pixel[0], pixel[1], pixel[2])

    @staticmethod
    def paint_two_pixels(top_color, bottom_color):
        print("{}{}{}{}{}".format(Viewer.to_fg(bottom_color), Viewer.to_bg(top_color), Viewer.two_pixels, fg.rs, bg.rs), end="")
