from libs.Module import Module


class AdminCount(Module):

    __name__ = 'Admins_Count'
    auto_exec = True
    online_temp = ''
    offline_temp = ''

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
            self.loadtemp()
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return self.updatechannel()

    def loadtemp(self):
        try:
            self.online_temp = open(self.config['General']['Text']).read()
            self.offline_temp = open(self.config['General']['Text_offline']).read()
        except Exception as er:
            self.auto_exec = False
            return self.error(er)

    def updatechannel(self):
        try:
            clientlist = self.conn.clientlist(away=True, uid=True, voice=True)
            admin_count = 0
            online_uid_list = []

            for sgid in self.config['General']['Groups'].split(','):
                for user in self.conn.servergroupclientlist(sgid=sgid, names=True):
                    admin_info = self.isonline(user['client_unique_identifier'], clientlist)
                    if admin_info:
                        if admin_info['client_unique_identifier'] in online_uid_list:
                            continue
                        if not admin_info['client_type'] == '0':
                            continue
                        if admin_info['client_away'] == '1' or admin_info['client_output_muted'] == '1':
                            if self.config['General']['Include_AFK'].upper() == 'TRUE':
                                admin_count += 1
                                online_uid_list.append(admin_info['client_unique_identifier'])
                                continue
                            else:
                                online_uid_list.append(admin_info['client_unique_identifier'])
                                continue
                        admin_count += 1
                        online_uid_list.append(admin_info['client_unique_identifier'])

            if admin_count > 0:
                channel_name = self.online_temp.format(admin_count=admin_count)
            else:
                channel_name = self.offline_temp.format(admin_count=admin_count)

            if self.config['General']['Mode'] == '1':
                kwa = {'channel_name': channel_name, 'cid': self.config['General']['Channel_ID']}
            elif self.config['General']['Mode'] == '2':
                kwa = {'channel_description': channel_name, 'cid': self.config['General']['Channel_ID']}
            else:
                return self.other['libs.Interval'].S.remove_job(self.__name__)

            try:
                return self.conn.channeledit(**kwa)
            except self.other['ts3.Error']:
                return
        except Exception as er:
            return self.error(er)
