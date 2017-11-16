from time import strftime
from apscheduler.triggers.interval import IntervalTrigger


class Module(object):

    config = None
    auto_exec = True
    __name__ = 'Unknown'
    conn = object

    def __init__(self, libs):
        self.other = libs
        self.loadconf()
        self.getconn()
        if self.auto_exec:
            self.joinjob(self.execute_, self.intervaltosec(), [])

    def getconn(self):
        self.conn = self.other['libs.Connect'].conn[self.config['General']['Instance']]

    def intervaltosec(self, conf='Interval'):
        hour = int(self.config[conf]['Hours']) + int(self.config[conf]['Days']*24)
        minutes = int(self.config[conf]['Minutes']) + hour*60
        return int(self.config[conf]['Seconds']) + minutes*60

    def loadconf(self):
        return None
        # Function to override

    def execute_(self):
        return None
        # Function to override

    def convert(self, time):
        try:
            time = int(time)
            day = int(time / 86400)
            hours = int((time - (day * 86400)) / 3600)
            minutes = int((time - ((day * 86400) + (hours * 3600))) / 60)
            convert = ""
            if day > 0:
                convert = convert + str(day)
                if day == 1:
                    convert = convert + " dzień "
                else:
                    convert = convert + " dni "
            if hours > 0:
                convert = convert + str(hours)
                if hours == 1:
                    convert = convert + " godzina "
                else:
                    convert = convert + " godzin "
            if minutes > 0:
                convert = convert + str(minutes)
                if minutes == 1:
                    convert = convert + " minuta "
                else:
                    convert = convert + " minut "
            return convert
        except Exception as er:
            self.error(er)
            return '%Error%'

    # def setinterval(self, time, func, arg):
    #    import threading
    #
    #    def func_wraper():
    #        self.setinterval(time, func, arg)
    #        func(*arg)
    #    threading.Timer(time, func_wraper).start()
    #    return

    def joinjob(self, func, sec=None, arg=None):
        self.other['libs.Interval'].S.add_job(func,
                                              IntervalTrigger(seconds=sec), arg,
                                              id=self.__name__, replace_existing=True)
        # self.setinterval(sec, func, arg)

    def replace(self, text='', data=None):
        if not data:
            data = self.conn.serverinfo()
            data = data.parsed[0]
        try:
            online = int(data['virtualserver_clientsonline']) - int(data['virtualserver_queryclientsonline'])
            return text.format(
                               online=online,
                               max=data['virtualserver_maxclients'],
                               hour=strftime('%H'),
                               minute=strftime('%M'),
                               ping=round(float(data['virtualserver_total_ping'])),
                               uptime=self.convert(data['virtualserver_uptime']),
                               channel=data['virtualserver_channelsonline'],
                               )
        except Exception as er:
            self.error(er)

    def isingroup(self, one='', two=''):
        try:
            return not list(set(one.split(',')).intersection(two.split(','))) == []
        except Exception as er:
            self.error(er)
            return []

    def isonline(self, uid, data=None):
        try:
            if not data:
                data = self.conn.clientlist()
            for client in data:
                if client['client_unique_identifier'] == uid:
                    return client
            return False
        except Exception as er:
            self.error(er)

    def groupname(self, sgid, data):
        try:
            for rank in data:
                if rank['sgid'] == sgid:
                    return rank['name']
            return ''
        except Exception as er:
            self.error(er)

    def error(self, err):
        self.other['libs.Logs'].addlog('warning', 'Moduł {} napotkał problem: {}'.format(self.__name__, err))
