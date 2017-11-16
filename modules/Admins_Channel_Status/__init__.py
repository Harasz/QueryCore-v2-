from modules.Admins_Channel_Status.source import AdminChannelStatus


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return AdminChannelStatus(*args, **kwargs)
