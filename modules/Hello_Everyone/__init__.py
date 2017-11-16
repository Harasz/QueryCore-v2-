from modules.Hello_Everyone.source import HelloEveryone


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return HelloEveryone(*args, **kwargs)
