from modules.Admins_List.source import AdminList


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return AdminList(*args, **kwargs)
