from configparser import ConfigParser


class ReadConf(object):

    other = {}
    config = ConfigParser()

    def __init__(self):
        self.config.read('QueryCore.conf')

    def getlibs(self, libs):
        self.other = libs
        self.checkconf()

    def checkconf(self):
        for key in self.config.sections():
            for value in self.config.items(key):
                if value[1] == '' or value[1] == ' ' or\
                        (value[0] == 'name' and len(value[1]) > 25):
                    self.other['libs.Logs'].addlog('warning',
                                                   '[Config] Wartość {} w sekcji {}, '
                                                   'wydaje się być nieprawidłowa!'.format(value[0], key))

    def loadconf(self, file):
        try:
            conf = ConfigParser()
            conf.read(file)
            return conf
        except Exception as er:
            self.other['libs.Logs'].addlog('danger', 'Read_Conf nie może odczytać konfiguracji {}: {}'.format(file, er))
