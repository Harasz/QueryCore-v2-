from libs.Module import Module


class AdminChannelStatus(Module):

    __name__ = 'Admins_Channel_Status'
    auto_exec = True

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return self.check()

    def check(self):
        try:
            client_list = self.conn.clientlist(uid=True, away=True, voice=True)
            for channel in self.conn.channellist(topic=True):
                topic_splited = channel['channel_topic'].split(',')
                if topic_splited[0] == 'acs':
                    online = self.isonline(topic_splited[1], client_list)
                    if online:
                        if online['client_away'] == '1' or online['client_output_muted'] == '1':
                            kwa = {'channel_name': self.config['General']['Display'].format(
                                status=self.config['General']['Afk'], channel_name=topic_splited[2])}
                        else:
                            kwa = {'channel_name': self.config['General']['Display'].format(
                                status=self.config['General']['Online'], channel_name=topic_splited[2])}
                    else:
                        kwa = {'channel_name': self.config['General']['Display'].format(
                            status=self.config['General']['Offline'], channel_name=topic_splited[2])}
                    try:
                        self.conn.channeledit(**kwa, cid=channel['cid'])
                    except self.other['ts3.Error'] as er:
                        if er.resp.error['id'] == '1541':
                            self.error('Za długa nazwa kanału dla: {}'.format(channel['cid']))
                            continue
                        elif er.resp.error['id'] == '771':
                            continue
                        else:
                            self.error(er)
                            continue
                else:
                    continue
            return
        except Exception as er:
            return self.error(er)
