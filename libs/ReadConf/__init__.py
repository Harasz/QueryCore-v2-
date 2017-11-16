from libs.ReadConf.source import ReadConf


class Loadfile(object):
    name = 'ReadConf'
    obj = 'ReadConf'

    def loadobj(*args, **kwargs):
        return ReadConf(*args, **kwargs)
