from modules.Channel_Checker.source import ChannelChecker


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return ChannelChecker(*args, **kwargs)
