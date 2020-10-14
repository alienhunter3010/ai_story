import yaml
import logging


class Config:
    config_file = 'var/evolution.yaml'

    @staticmethod
    def save(ai_setup):
        logging.info("Saving setup")
        with open(Config.config_file, 'w') as f:
            yaml.dump(ai_setup, f)

    @staticmethod
    def load():
        logging.info("Loading setup")
        with open(Config.config_file) as f:
            return yaml.load(f)


class Keys:
    key_file = 'etc/keys.yaml'
    keys = {}


    @staticmethod
    def load():
        logging.info("Loading keys")
        with open(Keys.key_file) as f:
            Keys.keys = yaml.load(f, Loader=yaml.Loader)

    @staticmethod
    def get(product):
        return Keys.keys[product]
