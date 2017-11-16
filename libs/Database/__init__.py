from libs.Database.source import Database


class Loadfile(object):
    name = 'Database'
    obj = 'Database'

    def loadobj(*args, **kwargs):
        return Database(*args, **kwargs)
