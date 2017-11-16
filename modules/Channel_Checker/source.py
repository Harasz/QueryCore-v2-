from libs.Module import Module
from datetime import datetime
from re import search


class ChannelChecker(Module):

    __name__ = 'Channel_Checker'
    auto_exec = True
    db = object

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
            if 'libs.Database' in self.other:
                self.db = self.other['libs.Database'].db[self.config['General']['Instance']].cursor()
                self.checkdatabes()
            else:
                self.auto_exec = False
                self.error('Brak wymaganej biblioteki Database')
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return self.start_check()

    def checkdatabes(self):
        try:
            self.db.execute("""
            CREATE TABLE IF NOT EXISTS channel_checker (
                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `cid`	TEXT NOT NULL,
                `date`	TEXT NOT NULL
            );
            """)
        except Exception as er:
            self.error(er)
        return

    def clear_db(self, channels, db):
        try:
            exist_cid = [ch['cid'] for ch in channels]
            db_cid = [d[0] for d in db]
            for key in set(db_cid) - set(exist_cid):
                self.db.execute("DELETE FROM channel_checker WHERE cid=?;", (key,))
        except Exception as er:
            return self.error(er)

    def start_check(self):
        try:
            channels_list = self.conn.channellist(limits=True)
            self.db.execute("SELECT cid, date FROM channel_checker;")
            db_list = self.db.fetchall()
            now = datetime.now()
            free_count = 0
            channel_close_expire = []
            cn = 0

            self.clear_db(channels_list, db_list)

            for channel in channels_list:
                if channel['pid'] == self.config['General']['Pid']:
                    cn = int(search(r'\d+', channel['channel_name']).group())
                    data_date = [db[1] for db in db_list if db[0] == channel['cid']]
                    if data_date:
                        if int(channel['total_clients']) > 0:
                            self.db.execute("UPDATE channel_checker SET date=? WHERE cid=?;",
                                            (now.strftime('%Y-%m-%d'), channel['cid']))
                        else:
                            if data_date[0] == 'Free':
                                if self.config['General']['Free_name'] in channel['channel_name']:
                                    free_count += 1
                                    continue
                                else:
                                    self.db.execute("UPDATE channel_checker SET date=? WHERE cid=?;",
                                                    (now.strftime('%Y-%m-%d'), channel['cid']))
                                    continue
                            delta = now - datetime.strptime(data_date[0], '%Y-%m-%d')
                            if delta.days >= int(self.config['General']['Days']):
                                self.conn.channeldelete(cid=channel['cid'], force=False)
                                self.conn.channelcreate(channel_maxclients=0, channel_flag_maxclients_unlimited=0,
                                                        channel_flag_permanent=1,
                                                        cpid=self.config['General']['Pid'],
                                                        channel_order=channel['channel_order'],
                                                        channel_name=search(r'\d+',
                                                                            channel['channel_name']).group() + '. ' +
                                                                            self.config['General']['Free_name'])
                                self.db.execute("DELETE FROM channel_checker WHERE cid=?;", (channel['cid'], ))
                                free_count += 1
                            elif delta.days >= int(self.config['General']['Days']) - 2:
                                channel_close_expire.append((channel['channel_name'], channel['cid']))
                            continue
                    else:
                        if self.config['General']['Free_name'] in channel['channel_name']:
                            status = 'Free'
                            free_count += 1
                        else:
                            status = now.strftime('%Y-%m-%d')
                        self.db.execute("INSERT INTO channel_checker VALUES (null, ?, ?);",
                                        (channel['cid'], status))

            if not self.config['General']['Close_expire'] == '0':
                desc = '[SIZE=18]Kanały do usunięcia[/SIZE]\n[SIZE=10](zostaną usunięte w przeciągu 48h)[/SIZE][LIST]'
                if channel_close_expire:
                    for channel in channel_close_expire:
                        desc += '[*][url=channelID://' + channel[1] + '] ' + channel[0] + '[/url]'
                else:
                    desc += '\n\n'
                desc += '[/LIST]\n\n[RIGHT]Generate by QueryCore - ' \
                        'TeamSpeak3 server control bot.\n© ALL RIGHTS RESERVED[/RIGHT]'
                channel_info = self.conn.channelinfo(cid=self.config['General']['Close_expire'])
                if not channel_info[0]['channel_description'] == desc:
                    self.conn.channeledit(cid=self.config['General']['Close_expire'], channel_description=desc)

            if free_count < int(self.config['General']['Free_count']):
                for i in range(int(self.config['General']['Free_count']) - free_count):
                    cid = i + 1 + cn
                    self.conn.channelcreate(channel_maxclients=0, channel_flag_maxclients_unlimited=0,
                                            channel_flag_permanent=1, cpid=self.config['General']['Pid'],
                                            channel_name=str(cid) + '. ' + self.config['General']['Free_name'])

        except Exception as er:
            return self.error(er)
