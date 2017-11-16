from libs.Interval.source import Interval


class Loadfile(object):
    name = 'Logs'
    obj = 'Logs'

    def loadobj(*args, **kwargs):
        return Interval(*args, **kwargs)
