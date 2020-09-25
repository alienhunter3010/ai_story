from aileen.Callbackable import Callbackable
from aileen.Remote import Remote
from aileen.Cluster import PluginCluster
from aileen.Handlers import Handlers
from aileen.plugin.Cli import Cli
from aileen.IO import IO

import time


class AIleen(Remote):

    def __init__(self):
        IO.print(" ** <ansiyellow>An AI story</ansiyellow> ** a python game <ansiwhite>by ACe</ansiwhite>")
        self.io = Cli()
        self.cluster = PluginCluster()
        super().__init__()

    def ask(self):
        while True:
            cmd = self.io.ask()
            if cmd is not None and cmd != '':
                break
            time.sleep(3)
        return cmd

    def exiting(self, goodbye='gOOd-bYe'):
        # TODO: Move it to Mind any 10 minutes
        #self.cluster.save_evolution(exiting=True)
        self.send_command(goodbye)
        for i in range(3):
            IO.print('.', end='')
            time.sleep(1)
        IO.print('\nBye bye')
        exit()

    def confirm(self, cmd):
        if cmd.endswith('!'):
            return True
        else:
            answer = self.io.ask("Are you sure [yN]?")
            if answer.startswith('y'):
                return True
        return False

    def run(self):
        self.connect()
        self.cluster.load_config(
            self.receive_answer()
        )
        while True:
            cmd = self.ask()
            if cmd.startswith('exit'):
                if self.confirm(cmd):
                    self.exiting()
                    break
                continue
            elif cmd.startswith('shUt-dOwn'):
                if self.confirm(cmd):
                    self.exiting(cmd)
                    break
                continue
            answer = Handlers.getInstance().exec_control(cmd)
            self.output(answer.get_dict() if answer.has_totalk() else self.solve(cmd))

    def output(self, answer):
        wtf = True
        for row in answer['rows']:
            wtf = False
            IO.print(row, mode=answer['style'] or 'HTML')
        for row in answer['raw_rows']:
            wtf = False
            print(row)
        # TODO: update behaviours from answer['setup']
        if 'parser' in answer['setup']:
            Callbackable.solve_callback(answer['setup']['parser'], self.cluster)(self.receive_binary(), arguments=Callbackable.optional(answer['setup'], 'arguments', None))
        elif 'local' in answer['setup']:
            Callbackable.solve_callback(answer['setup']['local'], self.cluster)(arguments=Callbackable.optional(answer['setup'], 'arguments', None))
        elif wtf:
            IO.print("Really, I don't know")

# Use `python3 -m aileen` to launch this interface