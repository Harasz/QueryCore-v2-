from modules.Admins_Count.source import AdminCount


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return AdminCount(*args, **kwargs)
