from libs.Module import Module


class HelloEveryone(Module):

    __name__ = 'Hello_Everyone'
    auto_exec = False
    mess = ''

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
        except Exception as er:
            return self.error(er)

    def execute_(self):
        self.getmess()
        return self.other['libs.EventManager'].registerfunc(self.getevent, self.config['General']['Instance'])

    def getmess(self):
        try:
            self.mess = open(self.config['General']['Path']).read()
            return
        except Exception as er:
            return self.error(er)

    def getevent(self, event):
        if 'reasonid' in event and event['reasonid'] == '0' and\
           'client_nickname' in event and event['client_type'] == '0':
            if self.config['General']['Mode'] == '1':
                return self.mode_1(event)
            elif self.config['General']['Mode'] == '2':
                return self.mode_2(event)
            elif self.config['General']['Mode'] == '3':
                return self.mode_3(event)

    def mode_1(self, event):
        try:
            msg = self.replace(self.mess, event)
            return self.conn.sendtextmessage(targetmode=1, target=event['clid'], msg=msg)
        except Exception as er:
            return self.error(er)

    def mode_2(self, event):
        try:
            if self.conn.clientinfo(clid=event['clid'])[0]['client_totalconnections'] == '0':
                msg = self.replace(self.mess, event)
                return self.conn.sendtextmessage(targetmode=1, target=event['clid'], msg=msg)
            return
        except Exception as er:
            return self.error(er)

    def mode_3(self, event):
        try:
            if self.isingroup(self.config['General']['Groups'], event['client_servergroups']):
                msg = self.replace(self.mess, event)
                return self.conn.sendtextmessage(targetmode=1, target=event['clid'], msg=msg)
            return
        except Exception as er:
            return self.error(er)

    def replace(self, text='', event=None):
        from time import strftime
        try:
            data = self.conn.serverinfo()
            data = data.parsed[0]
            online = int(data['virtualserver_clientsonline']) - int(data['virtualserver_queryclientsonline'])
            return text.format(
                               online=online,
                               max=data['virtualserver_maxclients'],
                               hour=strftime('%H'),
                               minute=strftime('%M'),
                               ping=round(float(data['virtualserver_total_ping'])),
                               uptime=self.convert(data['virtualserver_uptime']),
                               channel=data['virtualserver_channelsonline'],
                               client_nickname=event['client_nickname'],
                               client_unread_messages=event['client_unread_messages'],
                               client_unique_identifier=event['client_unique_identifier']
                               )
        except Exception as er:
            return self.error(er)
