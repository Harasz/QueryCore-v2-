from modules.AFK_Checker.source import AFkCheck


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return AFkCheck(*args, **kwargs)
