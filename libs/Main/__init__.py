from libs.Main.source import Startbot


class Loadfile(object):
    name = 'mainCLass'
    obj = 'MainClass'

    def loadobj(*args, **kwargs):
        return Startbot(*args, **kwargs)
