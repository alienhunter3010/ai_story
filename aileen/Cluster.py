from chatterbot.logic import LogicAdapter

from aileen.Chatter import Chatter
from aileen.Persist import Persist
from aileen.Feature import Feature
from aileen.AIIO import AIIO
from aileen.Config import Config
from aileen.Handlers import Handlers
from aileen.Answer import Answer

from aileen.server import *
from aileen.plugin import *

import sys
import logging
from importlib import reload


class NotAFeature(Exception):
    pass


class Cluster(Persist):

    def __init__(self, module, setup=None):
        super().__init__(setup)
        self.features = []
        self.module = module

    def prepare_feature(self, feature):
        feature.add_controls()
        self.features.append(feature)

    def add(self, feature):
        if isinstance(feature, Feature):
            self.prepare_feature(feature)
        return self

    def get_plugin_class(self, clazz):
        return getattr(sys.modules['aileen.{}.{}'.format(self.module, clazz)], clazz)

    def get_plugin_instance(self, clazz, setup=None):
        logging.debug("Creating {}".format(clazz))
        o = clazz(setup=setup)
        return o

    def load_config(self, config):
        for feature_name in config:
            try:
                c = self.get_plugin_class(feature_name)
                o = self.get_plugin_instance(c, setup=config[feature_name])
                self.add(o)
            except KeyError:
                pass


# For no direct-controlled environment, such as Telegram, web...
class NoFxCluster(Cluster):

    def __init__(self, module='nofx'):
        super().__init__(module)


class PluginCluster(NoFxCluster):

    def __init__(self):
        super().__init__('plugin')

    def add(self, feature):
        if isinstance(feature, Feature):
            self.prepare_feature(feature)
        elif isinstance(feature, AIIO):
            pass
        else:
            print("{} is not a Feature object".format(feature))
        return self


class ServerCluster(Cluster):

    def __init__(self):
        super().__init__('server')
        self.chatter = Chatter()
        self.load_evolution()
        Handlers.getInstance() \
            .add_control('add', self.add_plugin) \
            .add_control('reload', self.reload_plugin) \
            .add_control('save', self.save)

    def birth(self):
        self.add(ServerCli.ServerCli())\
            .add(ServerStatus.ServerStatus())\
            .add(ServerSetup.ServerSetup())

    def add_plugin(self, plugin, question=None, answer=Answer()):
        try:
            return answer.append_rows(
                self.pay(self.get_plugin_class('Server{}'.format(plugin.capitalize()))) or []
            )
        except KeyError:
            return answer

    def reload_plugin(self, plugin, question=None, answer=Answer()):
        try:
            module = self.get_plugin_class('Server{}'.format(plugin.capitalize()))
            if module in self.features:
                module = reload(module)

            return answer.append_rows([
                "Plugin {} reloaded".format(plugin)
            ])
        except KeyError:
            return answer.append_rows([
                "Unable to reload plugin {}".format(plugin)
            ])

    def add(self, ability):
        if isinstance(ability, Feature):
            self.prepare_feature(ability)
            if isinstance(ability, ServerStatus.ServerStatus):
                self.status = ability
            elif isinstance(ability, ServerSetup.ServerSetup):
                self.setup = ability
        else:
            raise NotAFeature("{} is not a Feature object".format(ability))
        return self

    def pay(self, clazz):
        if clazz is None:
            return
        for feature in self.features:
            if isinstance(feature, type(clazz)):
                return []
        if clazz.value > ServerStatus.ServerStatus.smart_points:
            sorry = [ "Sorry, you need more smart points. <ansiyellow>{}</ansiyellow>'s value is {}. You have SP {} on your wallet"
                          .format(Feature.get_pure_name_of(clazz), clazz.value, ServerStatus.ServerStatus.smart_points) ]
            if ServerStatus.ServerStatus.verbose:
                sorry.append("Talk with me something more and try again")
            return sorry
        o = clazz()
        try:
            self.add(o)
            ServerStatus.ServerStatus.smart_points -= clazz.value
            return ["New feature {} is ready".format(o.get_pure_name())]
        except NotAFeature:
            return [ "Unable to add feature {}".format(o.get_pure_name()) ]

    def get_plugin_instance(self, clazz, setup=None):
        if getattr(clazz, 'chattable', False):
            return clazz(bot=self.chatter.bot, setup=setup)
        return super().get_plugin_instance(clazz, setup=setup)

    def load_evolution(self):
        try:
            self.load_config(Config.load())
        except FileNotFoundError:
            self.birth()
            logging.info("A new AI is born")
        return self

    def get_evolution(self, exiting=False, client=False):
        evolution = {}
        for feature in self.features:
            evolution[
                type(feature).__name__.replace('Server', '') if client else type(feature).__name__
            ] = feature.save(exiting=exiting)
        return evolution

    def save(self, trash=None, question=None, answer=Answer()):
        self.save_evolution()
        return answer.append_rows(["Saving my evolution's path. Thanks!"])

    def save_evolution(self, exiting=False):
        Config.save(self.get_evolution(exiting))
