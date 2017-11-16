from apscheduler.triggers.date import DateTrigger


class EventManager(object):

    other = {}
    regfunc = {}
    regconn = {}
    lastevent = {}

    def getlibs(self, libs):
        self.other = libs
        self.regfunc = {}
        self.regconn = {}
        self.lastevent = {}

    def waitforevent(self, conn_name):
        while True:
            try:
                event = self.regconn[conn_name].wait_for_event(timeout=550)
            except AttributeError:
                break
            except Exception as er:
                self.other['libs.Logs'].addlog('warning', 'Event Manager napotkał błąd: {}'.format(er))
            else:
                if self.lastevent[conn_name] == event[0]:
                    continue
                else:
                    self.lastevent[conn_name] = event[0]
                for func in self.regfunc[conn_name]:
                    func(event[0])

    def registerconn(self, conn, name):
        import datetime
        if name not in self.regconn:
            conn.servernotifyregister(event='channel', id_=0)
            self.regconn[name] = conn
            self.regfunc[name] = []
            self.lastevent[name] = None
            self.other['libs.Interval'].S.add_job(self.waitforevent,
                                                  DateTrigger(datetime.datetime.today()+datetime.timedelta(minutes=1)),
                                                  args=[name], id='Event_{}'.format(name))
        return

    def registerfunc(self, func, conn_name):
        if conn_name in self.regconn:
            self.regfunc[conn_name].append(func)
        else:
            self.other['libs.Logs'].addlog('warning', 'Połączenie {} nie obsługuje Eventów'.format(conn_name))
        return
