from aileen.Feature import Feature
from aileen.Answer import Answer
from aileen.Handlers import Handlers
from aileen.intersect.TupleForOutput import TupleOut

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr


class ServerWolfram(Feature):
    value = 50

    def __init__(self):
        self.session = WolframLanguageSession()

    def __del__(self):
        self.session.stop()
        self.session.terminate()

    def wolfram_try(self, payload, mode="SpokenResult", gatling=("ShortAnswer", "Result"), answer=Answer()):
        wlf = self.session.evaluate(wl.WolframAlpha(payload, mode))
        if isinstance(wlf, str):
            return self.echo(wlf, answer)
        elif "No{}".format(mode) in wlf.args:
            return self.wolfram_try(payload, mode=gatling[0], gatling=gatling[1:], answer=answer)
        return self.echo(self.readable(wlf), answer)

    def wolfram_alpha(self, payload, question=None, answer=Answer()):
        return self.wolfram_try(payload, answer=answer)

    def wolframify(self, trash, question=None, answer=Answer()):
        if answer.has_totalk():
            return answer
        return self.wolfram_alpha(question, answer=answer)

    def greetings(self, trash, question=None, answer=Answer()):
        return self.echo(
            "\t<code>Wolfram</code> plugin use Wolfram's Python library to interact with <b>wolframalpha.com</b> APIs",
            answer
        )

    def wl(self, expr, question=None, answer=Answer()):
        return self.echo( self.readable(
            self.session.evaluate(wlexpr(expr))
        ))

    def help(self, trash, question=None, answer=Answer()):
        return answer.append_rows([
            "\n  <bold>Wolfram commands:</bold>",
            "\t<pre>wl (expr)</pre>\tEvaluate a Wolfram Language expression",
            "\t<pre>.?</pre>\tAny unknown question is now parsed by Wolfram Alpha engine",
        ])

    def add_controls(self):
        Handlers.getInstance() \
            .add_control('wl', self.wl) \
            .add_control('greetings', self.greetings) \
            .add_control('help', self.help) \
            .add_control('wa', self.wolfram_alpha) \
            .add_control('.*', self.wolframify)

    def readable(self, tpl):
        return TupleOut.joint(tpl, armored=False)

