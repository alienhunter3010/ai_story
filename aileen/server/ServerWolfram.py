import logging

from aileen.Chatter import PluggableAdapters, AutoAdapter
from aileen.Answer import Answer
from aileen.Handlers import Handlers
from aileen.intersect.TupleForOutput import TupleOut

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

import re


class ServerWolfram(PluggableAdapters):
    value = 50
    session = None

    def __init__(self, bot=None, setup=None, **kwargs):
        super().__init__(bot=bot, setup=setup, **kwargs)
        ServerWolfram.session = WolframLanguageSession()

    def __del__(self):
        ServerWolfram.session.stop()
        ServerWolfram.session.terminate()

    def register_adapters(self, bot, **kwargs):
        self.inject_adapter(bot, WaAdapter)\
            .inject_adapter(bot, WlAdapter)

    def greetings(self, trash, question=None, answer=Answer()):
        return self.echo(
            "\t<code>Wolfram</code> plugin use Wolfram's Python library to interact with <b>wolframalpha.com</b> APIs",
            answer
        )

    def help(self, trash, question=None, answer=Answer()):
        return answer.append_rows([
            "\n  <bold>Wolfram commands:</bold>",
            "\t<pre>wl (expr)</pre>\tEvaluate a Wolfram Language expression",
            "\t<pre>.?</pre>\tAny unknown question is now parsed by Wolfram Alpha engine",
        ])

    def add_controls(self):
        Handlers.getInstance() \
            .add_control('greetings', self.greetings) \
            .add_control('help', self.help) \


#
# Adapters
#


class WolframAdapter(AutoAdapter):
    def __init__(self, bot=None, command='wa', **kwargs):
        super().__init__(bot, **kwargs)
        self.rcut = re.compile(r"^{} ".format(command), re.IGNORECASE)

    def wolfram_try(self, payload, mode="SpokenResult", gatling=("ShortAnswer", None)):
        wlf = ServerWolfram.session.evaluate(wl.WolframAlpha(payload)) \
                if mode is None else ServerWolfram.session.evaluate(wl.WolframAlpha(payload, mode))
        if isinstance(wlf, str):
            return wlf
        elif type(wlf) is tuple:
            return self.readable(wlf)
        elif wlf is None or "No{}".format(mode) in wlf.args:
            if len(gatling) == 0:
                return ""
            return self.wolfram_try(payload, mode=gatling[0], gatling=gatling[1:])
        return ""

    def readable(self, tpl):
        if len(tpl) > 0 and len(tpl[-1]) > 0:
            return tpl[-1][1]
        # return ''
        return TupleOut.joint(tpl, armored=False)


class WaAdapter(WolframAdapter):

    def __init__(self, bot=None, setup=None, **kwargs):
        super().__init__(bot=bot, command="wa", **kwargs)

    def can_process(self, statement):
        return True

    def process(self, input_statement, additional_response_selection_parameters=None):
        result = super().process(input_statement, additional_response_selection_parameters)
        result.text = self.wolfram_alpha(self.rcut.sub('', input_statement.text))

        if isinstance(result.text, str) and len(result.text) > 10:
            result.confidence = 1 if input_statement.text.startswith('wa ') else 0.8
        else:
            result = super().process(input_statement, additional_response_selection_parameters)
        return result

    def wolfram_alpha(self, payload):
        return self.wolfram_try(payload)


class WlAdapter(WolframAdapter):

    def __init__(self, bot=None, setup=None, **kwargs):
        super().__init__(bot=bot, command="wl", **kwargs)

    def can_process(self, statement):
        if statement.text.startswith('wl '):
            return True
        return False

    def process(self, input_statement, additional_response_selection_parameters=None):
        result = super().process(input_statement, additional_response_selection_parameters)
        result.text = self.wl(input_statement.text.replace('wl ', ''))
        result.confidence = 1 if len(result.text) > 0 else 0
        return result

    def wl(self, expr):
        return self.readable(
            ServerWolfram.session.evaluate(wlexpr(self.rcut.sub('', expr)))
        )
