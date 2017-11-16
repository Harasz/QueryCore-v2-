from libs.Module import Module


class ServerProp(Module):

    available = True
    message = ''
    __name__ = 'Server_Property'
    auto_exec = True

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
        except Exception as er:
            return self.error(er)

    def execute_(self):
        self.updatehost()
        return

    def getmessage(self):
        try:
            message = open(self.config['Host_Message']['Path'], 'r').read()

            if len(message) > 200:
                self.other['libs.Logs'].addlog('warning',
                                               'Wiadomośc hosta jest za długa. Dopuszczalna ilość znaków to 200.')
                self.available = False
                return
            self.message = message
            return
        except Exception as er:
                return self.error(er)

    def updatehost(self):
        try:
            kwargs = {}

            if self.config['Host_Message']['Active'] == 'True' and self.available:
                kwargs['virtualserver_hostmessage'] = self.message
                for va in ('{online}', '{max}', '{uptime}', '{minute}', '{hour}', '{ping}', '{channel}'):
                    if va in self.message:
                        kwargs['virtualserver_hostmessage'] = self.replace(self.message)
                        break
                kwargs['virtualserver_hostmessage_mode'] = self.config['Host_Message']['Mode']

            if self.config['Server_name']['Active'] == 'True':
                for va in ('{online}', '{max}', '{uptime}', '{minute}', '{hour}', '{ping}', '{channel}'):
                    if va in self.config['Server_name']['Name']:
                        kwargs['virtualserver_name'] = self.replace(self.config['Server_name']['Name'])
                        break

            return self.conn.serveredit(**kwargs)
        except Exception as er:
            return self.error(er)
