from libs.Module import Module


class NicknameChecker(Module):

    __name__ = 'Nickname_Checker'
    auto_exec = True
    mess = ''

    def loadconf(self):
        import os
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
            return self.getmess()
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return self.startcheck()

    def getmess(self):
        try:
            self.mess = open(self.config['General']['Path_1']).read()
        except Exception as er:
            return self.error(er)

    def startcheck(self):
        try:
            clientlist = self.conn.clientlist(groups=True)
            words = open(self.config['General']['Path_2']).read()
            for client in clientlist:
                if not client['client_type'] == '0' or \
                        self.isingroup(self.config['General']['Group'], client['client_servergroups']):
                    continue

                for word in words.split('\n'):
                    if client['client_nickname'].find(word) == 0:
                        try:
                            self.conn.clientkick(clid=client['clid'],
                                                 reasonid=5,
                                                 reasonmsg=self.mess.format(bad_word=word))
                        except self.other['ts3.Error'] as er:
                            self.error(er)
                            continue
            return
        except Exception as er:
            return self.error(er)
