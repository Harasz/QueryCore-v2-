from modules.Server_Property.source import ServerProp


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return ServerProp(*args, **kwargs)
