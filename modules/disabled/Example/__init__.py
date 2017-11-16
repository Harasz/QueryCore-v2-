from modules.Global_Advertising import GlobalAdvert


class Loadfile(object):
    name = 'GlobalAdvert'
    obj = 'GlobalAdvert'

    def loadobj(*args, **kwargs):
        return GlobalAdvert(*args, **kwargs)
