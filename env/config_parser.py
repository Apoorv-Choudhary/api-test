import yaml


class ConfigParser:
    def __init__(self):
        self.config_data = {}
        with open("config.yaml", 'r') as stream:
            self.config_data = yaml.safe_load(stream)

