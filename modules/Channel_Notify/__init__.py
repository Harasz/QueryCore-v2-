from modules.Channel_Notify.source import ChannelNotify


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return ChannelNotify(*args, **kwargs)
