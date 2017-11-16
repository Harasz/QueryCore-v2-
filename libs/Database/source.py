import sqlite3


class Database(object):

    other = {}
    db = {}

    def init(self):
        self.other['libs.Logs'].addlog('info', '[Database] Baza danych została wczytana')
        return

    def add_database(self, name):
        try:
            db = sqlite3.connect('data/database', check_same_thread=False)
            db.isolation_level = None
            self.other['libs.Logs'].addlog('info', '[Database] Baza danych została wczytana dla {}'.format(name))
            self.db[name] = db
        except Exception as er:
            self.other['libs.Logs'].addlog('danger',
                                           '[Database] Baza danych nie została wczytana dla {}: {}'.format(name, er))

    def getlibs(self, libs):
        self.other = libs
        self.init()
