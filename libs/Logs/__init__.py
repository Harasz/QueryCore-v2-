from libs.Logs.source import Logs


class Loadfile(object):
    name = 'Logs'
    obj = 'Logs'

    def loadobj(*args, **kwargs):
        return Logs(*args, **kwargs)
