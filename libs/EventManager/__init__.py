from libs.EventManager.source import EventManager


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return EventManager(*args, **kwargs)
