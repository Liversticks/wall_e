
import os
import json
import configparser

config_file_location_local = "resources/utilities/config/local.ini"
config_file_location_prouction = "resources/utilities/config/production.ini"
config_file_location_dev = "resources/utilities/config/dev.ini"

cog_json_location = "resouces/cogs/cogs.json"
cog_location = "resources.cogs."

class WalleConfig():
    def __init__(self, environment):
        config = configparser.ConfigParser()
        config.optionxform = str
        if (environment == "LOCALHOST"):
            config.read(config_file_location_local)
        elif (environment == 'DEV'):
            config.read(config_file_location_dev)
        elif (environment == "PRODUCTION"):
            config.read(config_file_location_prouction)
        else:
            print("incorrect environment specified {}".format(environment))
        self.config = {}
        self.config['wall_e'] = config

    def get_config_value(self, section, option):
        if option in os.environ:
            return os.environ[option]

        if self.config['wall_e'].has_option(section, option):
            return self.config['wall_e'].get(section, option)
        return 'NONE'

    def set_config_value(self, section, name, value):
        if self.config['wall_e'].has_option(section, name):
            self.config['wall_e'].set(section, name, str(value))
        else:
            raise KeyError("Section '{}' or Option '{}' does not exist".format(section, name))

    def cog_enabled(self, name_of_cog):
        return (self.config['cogs_enabled'][name_of_cog] == 1);

    def get_cogs(self):
        cogs_to_load = []
        cogs = self.config['wall_e']
        for cog in cogs['cogs_enabled']:
            if int(cogs['cogs_enabled'][cog]) == 1:
                cogDict = {}
                cogDict['name'] = cog
                cogDict['path'] = cog_location
                cogs_to_load.append(cogDict)
        return cogs_to_load
