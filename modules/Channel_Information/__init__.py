from modules.Channel_Information.source import ChannelInfo


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return ChannelInfo(*args, **kwargs)
