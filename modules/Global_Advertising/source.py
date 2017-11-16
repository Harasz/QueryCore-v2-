from libs.Module import Module


class GlobalAdvert(Module):

    adv = []
    __name__ = 'Global_Advertising'
    auto_exec = False

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return self.loadmess()

    def loadmess(self):
        try:
            for message in self.config.sections()[1:]:
                tmp = open(self.config[message]['Path'], 'r').read()
                self.joinjob(self.globaladvert, self.intervaltosec(message), [tmp])
                self.globaladvert(tmp)
            return
        except Exception as er:
            return self.error(er)

    def globaladvert(self, message):
        try:
            for va in ('{online}', '{max}', '{uptime}', '{minute}', '{hour}', '{ping}', '{channel}'):
                if va in message:
                    message = self.replace(message)
                    break

            self.conn.sendtextmessage(targetmode=3, target=1, msg=message)
            return
        except Exception as er:
            return self.error(er)
