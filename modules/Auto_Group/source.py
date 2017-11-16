from libs.Module import Module


class AutoGroup(Module):

    __name__ = 'Auto_Group'
    auto_exec = False

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return self.other['libs.EventManager'].registerfunc(self.getevent, self.config['General']['Instance'])

    def getevent(self, event):
        if 'reasonid' in event and event['reasonid'] == '0' and 'ctid' in event and 'clid' in event:
            for cid in self.config.items('Auto_add'):
                if event['ctid'] == cid[0]:
                    return self.addgroup(event, cid[1])
            return

    def addgroup(self, ev, gid):
        try:
            client_info = self.conn.clientinfo(clid=ev['clid'])[0]
            if self.isingroup(client_info['client_servergroups'], gid):
                self.conn.clientkick(clid=ev['clid'], reasonid=4,
                                     reasonmsg='Jesteś już członkiem grupy {}'.format(
                                         self.groupname(gid, self.conn.servergrouplist())))
                return
            else:
                msg = 'Grupa {} została Ci nadana'.format(
                                         self.groupname(gid, self.conn.servergrouplist()))
                self.conn.servergroupaddclient(sgid=gid, cldbid=client_info['client_database_id'])
                self.conn.clientpoke(clid=ev['clid'], msg=msg)
                self.conn.clientkick(clid=ev['clid'], reasonid=4,
                                     reasonmsg=msg)
            return
        except Exception as er:
            return self.error(er)
