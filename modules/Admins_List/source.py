from libs.Module import Module
from datetime import datetime


class AdminList(Module):

    __name__ = 'Admins_List'
    auto_exec = True
    online_temp = ''
    offline_temp = ''
    desc = ''

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
            self.loadtemp()
        except Exception as er:
            return self.error(er)

    def execute_(self):
        self.desc = ''
        return self.getgroup()

    def loadtemp(self):
        try:
            self.online_temp = open(self.config['General']['Path_1']).read()
            self.offline_temp = open(self.config['General']['Path_2']).read()
        except Exception as er:
            return self.error(er)

    def convert_online(self, time):
        try:
            time = int(float(time) / float(1000))
            hours = int(time / float(3600))
            minutes = int((time / float(60)) % 60)
            convert = ""
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
            return ''

    def getgroup(self):
        try:
            clientlist = self.conn.clientlist(away=True, uid=True, voice=True)
            group_list = self.conn.servergrouplist()
            channel_list = self.conn.channellist()

            def channel_name(cid):
                for channel in channel_list:
                    if channel['cid'] == cid:
                        return '[URL=channelid://'+cid+']'+channel['channel_name']+'[/URL]'
                    return ''

            for sgid in self.config.sections()[2:]:
                self.desc = self.desc + self.config[sgid]['Name'].format(
                    rank_name=self.groupname(sgid=sgid, data=group_list))
                self.desc = self.desc + '[LIST]'
                for user in self.conn.servergroupclientlist(sgid=sgid, names=True):
                    admin_info = self.isonline(user['client_unique_identifier'], clientlist)
                    if admin_info:
                        if not admin_info['client_type'] == '0':
                            continue
                        if admin_info['client_away'] == '1' or admin_info['client_output_muted'] == '1':
                            status = '[COLOR=#CA8700]Chwilowo niedostępny[/COLOR]'
                        else:
                            status = '[COLOR=#347C17]Dostępny[/COLOR]'

                        self.desc = self.desc + self.online_temp.format(
                            client_nickname='[URL=client://' + admin_info['client_database_id'] + '/' + admin_info[
                                'client_unique_identifier'] + ']' + admin_info['client_nickname'] + '[/URL]',
                            status=status,
                            channel=channel_name(admin_info['cid']),
                            online_time=self.convert_online(
                                self.conn.clientinfo(
                                    clid=admin_info['clid'])[0]['connection_connected_time'])
                        )
                    else:
                        db_info = self.conn.clientdbinfo(cldbid=user['cldbid'])[0]
                        self.desc = self.desc + self.offline_temp.format(
                            status='[COLOR=red]Niedostępny[/COLOR]',
                            client_nickname='[URL=client://' + db_info['client_database_id'] + '/' + db_info[
                                'client_unique_identifier'] + ']' + db_info['client_nickname'] + '[/URL]',
                            last_connection=datetime.fromtimestamp(
                                int(db_info['client_lastconnected'])).strftime('%Y-%m-%d %H:%M'))
                self.desc = self.desc + '[/LIST]'
            return self.channeledit()
        except Exception as er:
            return self.error(er)

    def channeledit(self):
        try:
            self.desc = self.desc + '\n\n[RIGHT]Generate by QueryCore - ' \
                                    'TeamSpeak3 server control bot.\n© ALL RIGHTS RESERVED[/RIGHT]'
            return self.conn.channeledit(channel_description=self.desc, cid=self.config['General']['Channel_ID'])
        except Exception as er:
            return self.error(er)
