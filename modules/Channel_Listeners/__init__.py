from modules.Channel_Listeners.source import ChannelListeners


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return ChannelListeners(*args, **kwargs)
