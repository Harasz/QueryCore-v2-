from libs.Connect.source import ConnServer


class Loadfile(object):
    name = 'connect'
    obj = 'connect'

    def loadobj(*args, **kwargs):
        return ConnServer(*args, **kwargs)
