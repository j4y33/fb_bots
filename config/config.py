import configparser

section_names = 'logging', 'postgres', 'facebook', 'sms', 'vpn', 'proxy', 'platform', 'files', 'browser', 'image_api'


class Configuration(object):

    def __init__(self, *file_names):
        parser = configparser.ConfigParser()
        parser.optionxform = str
        found = parser.read(file_names)
        if not found:
            raise ValueError('No config file found!')
        for name in section_names:
            self.__dict__.update(parser.items(name))


config = Configuration('config/config.cfg')
