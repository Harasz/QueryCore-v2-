from libs.Module import Module
from time import strftime


class ChannelInfo(Module):

    data = {}
    __name__ = 'Channel_Information'
    auto_exec = True
    record = '0'
    cid = ''

    def loadconf(self):
        import os
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
            self.readrecord()
        except Exception as er:
            return self.error(er)

    def execute_(self):
        self.getdata()
        return self.readch()

    def getdata(self):
        try:
            self.data = self.conn.serverinfo()[0]
            return
        except self.other['ts3.Error'] as er:
            return self.error(er)

    def replace(self, text='', data=None):
        try:
            if '{record}' in text:
                record = self.getrecord()
            else:
                record = 0
            online = int(self.data['virtualserver_clientsonline']) - int(self.data['virtualserver_queryclientsonline'])
            return text.format(
                               record=record,
                               online=online,
                               max=self.data['virtualserver_maxclients'],
                               hour=strftime('%H'),
                               minute=strftime('%M'),
                               ping=round(float(self.data['virtualserver_total_ping'])),
                               uptime=self.convert(self.data['virtualserver_uptime']),
                               channel=self.data['virtualserver_channelsonline'],
                               )
        except Exception as er:
            return self.error(er)

    def readch(self):
        for cid in self.config.sections()[2:]:
            try:
                self.cid = cid
                self.conn.channeledit(
                    cid=cid,
                    channel_name=self.replace(self.config[cid]['Name'])
                )
            except self.other['ts3.Error']:
                continue
            except Exception as er:
                return self.error(er)
        return

    def getrecord(self):
        try:
            online = int(self.data['virtualserver_clientsonline']) - int(self.data['virtualserver_queryclientsonline'])
            if online > int(self.record):
                try:
                    desc = open(self.config[self.cid]['Path']).read().format(
                        record=online,
                        date=strftime('%d-%m-%Y, %H:%M')
                    ) + '\n\nGenerate by QueryCore - TeamSpeak3 server control bot.'
                    self.conn.channeledit(cid=self.cid,
                                          channel_description=desc)
                except (Exception, ):
                    pass
                open('modules/Channel_Information/record.dat', 'w').write(str(online))
                return online
            else:
                return self.record
        except Exception as er:
            return self.error(er)

    def readrecord(self):
        try:
            record = open('modules/Channel_Information/record.dat', 'r').read()
            if record == '':
                open('modules/Channel_Information/record.dat', 'w').write('0')
                return
            self.record = record
            return
        except Exception as er:
            return self.error(er)
