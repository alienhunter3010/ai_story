from prompt_toolkit import print_formatted_text
from prompt_toolkit import HTML, ANSI
from prompt_toolkit.styles import Style


class IO:
    style = Style.from_dict({
        '': '#ffffff bold'
    })

    @staticmethod
    def print(message, mode="HTML", end='\n'):
        IO.printHTML(message, end=end) if mode == 'HTML' else IO.printANSI(message, end=end)

    @staticmethod
    def printHTML(message, end='\n'):
        print_formatted_text(HTML(message), style=IO.style, end=end)

    @staticmethod
    def printANSI(message, end='\n'):
        print_formatted_text(ANSI(message), style=IO.style, end=end)