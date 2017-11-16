from libs.Module import Module


class ChannelNotify(Module):

    __name__ = 'Channel_Notify'
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
            if event['ctid'] in self.config.sections()[1:]:
                return self.channel(event)
            else:
                return

    def channel(self, event):
        try:
            clientlist = self.conn.clientlist(uid=True, voice=True, away=True)
            admins_online = []
            for sgid in self.config[event['ctid']]['Admin'].split(','):
                for admin in self.conn.servergroupclientlist(sgid=sgid, names=True):
                    online = self.isonline(admin['client_unique_identifier'], clientlist)
                    if online:
                        if online['cid'] == event['ctid']:
                            return
                        if online['client_away'] == '1' or online['client_output_muted'] == '1' or\
                                not online['client_type'] == '0':
                            continue
                        if online not in admins_online:
                            admins_online.append(online)

            mess = self.editmess(event['ctid'], admins_online, [x for x in clientlist if x['clid'] == event['clid']][0])

            if self.config[event['ctid']]['Mode'] == '1':
                return self.mode1(admins_online, event, mess)
            elif self.config[event['ctid']]['Mode'] == '2':
                return self.mode2(admins_online, event, mess)
            elif self.config[event['ctid']]['Mode'] == '3':
                return self.mode3(admins_online, event, mess)

            return self.other['libs.Logs'].addlog('warning',
                                                  '{} - Błąd w konfiguracji kanału {}'.format(self.__name__,
                                                                                              event['ctid']))
        except Exception as er:
            self.error(er)

    def editmess(self, cid, admins, user):
        admin_list = ''
        mess_1 = open(self.config[cid]['Path_1']).read()
        mess_2 = open(self.config[cid]['Path_3']).read()

        for admin in admins:
            admin_list = admin_list+'[URL=client://'+admin['client_database_id']\
                         + '/' + admin['client_unique_identifier']+']'+admin['client_nickname']+'[/URL], '
        if not admins:
            admin_list = 'Brak'
            mess_1 = open(self.config[cid]['Path_2']).read()
        mess_1 = mess_1.format(admin_list=admin_list, admin_count=len(admins))
        mess_2 = mess_2.format(
            user_nickname='[URL=client://'+user['client_database_id']+'/' + user['client_unique_identifier']+']' +
                          user['client_nickname']+'[/URL], '
                     )

        return [mess_1, mess_2]

    def mode1(self, admins, ev, mess):
        try:
            self.conn.sendtextmessage(targetmode=1, target=ev['clid'], msg=mess[0])
            for admin in admins:
                self.conn.sendtextmessage(targetmode=1, target=admin['clid'], msg=mess[1])
        except Exception as er:
            self.error(er)
        finally:
            return 

    def mode2(self, admins, ev, mess):
        try:
            self.conn.sendtextmessage(targetmode=1, target=ev['clid'], msg=mess[0])
            for admin in admins:
                self.conn.clientpoke(msg=mess[1], clid=admin['clid'])
        except Exception as er:
            self.error(er)
        finally:
            return 

    def mode3(self, admins, ev, mess):
        try:
            self.conn.clientpoke(msg=mess[0], clid=ev['clid'])
            for admin in admins:
                self.conn.clientpoke(msg=mess[1], clid=admin['clid'])
        except Exception as er:
            self.error(er)
        finally:
            return 
