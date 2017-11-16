from libs.Module import Module


class AFkCheck(Module):

    __name__ = 'AFK_Checker'
    auto_exec = True
    db = object

    def loadconf(self):
        try:
            self.config = self.other['libs.ReadConf'].loadconf('modules/{}/module.conf'.format(self.__name__))
            self.db = self.other['libs.Database'].db[self.config['General']['Instance']].cursor()
            self.checkdatabes()
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return self.check()

    def checkdatabes(self):
        try:
            self.db.execute("""
            CREATE TABLE IF NOT EXISTS afk_client_cache (
                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `clid`	TEXT NOT NULL,
                `cid`	TEXT NOT NULL
            );
            """)
        except Exception as er:
            self.error(er)
        return

    def cleardb(self, cl, cache):
        try:
            if not cache:
                return
            for clid in cache:
                if [1 for c in cl if c['clid'] == clid[0]]:
                    continue
                else:
                    self.db.execute("DELETE FROM afk_client_cache WHERE clid=?;", clid[0])
            return
        except Exception as er:
            self.error(er)

    def check(self):
        try:
            clientlist = self.conn.clientlist(away=True, voice=True, times=True, groups=True, uid=True)
            self.db.execute("SELECT clid FROM afk_client_cache;")
            cache = self.db.fetchall()
            self.cleardb(clientlist, cache)

            for client in clientlist:
                if client['client_away'] == '1' or client['client_output_muted'] == '1' or \
                        int(client['client_idle_time']) > int(self.config['General']['Idle_time'])*60000:
                    if not self.isingroup(client['client_servergroups'],
                                          self.config['General']['Ignore']+','+self.config['General']['Add_client']) or\
                       not client['cid'] == self.config['General']['Move_client']:
                        if not self.config['General']['Move_client'] == '0':
                            self.db.execute("INSERT INTO afk_client_cache VALUES (null, ?, ?);",
                                            (client['clid'], client['cid']))
                            try:
                                self.conn.clientmove(clid=client['clid'], cid=self.config['General']['Move_client'])
                            except self.other['ts3.Error']:
                                pass
                        if not self.config['General']['Add_client'] == '0':
                            try:
                                self.conn.servergroupaddclient(sgid=self.config['General']['Add_client'],
                                                               cldbid=client['client_database_id'])
                            except self.other['ts3.Error']:
                                pass
                        continue
                    else:
                        continue
                else:
                    if not cache:
                        continue
                    if [1 for c in cache if c[0] == client['clid']]:
                        if not self.config['General']['Move_client'] == '0':
                            self.db.execute("SELECT cid FROM afk_client_cache WHERE clid=?;", client['clid'])
                            cid = self.db.fetchone()
                            if client['cid'] == self.config['General']['Move_client']:
                                try:
                                    self.conn.clientmove(clid=client['clid'], cid=cid[0])
                                except self.other['ts3.Error']:
                                    pass
                            self.db.execute("DELETE FROM afk_client_cache WHERE clid=?;", client['clid'])
                        if not self.config['General']['Add_client'] == '0':
                            try:
                                self.conn.servergroupdelclient(sgid=self.config['General']['Add_client'],
                                                               cldbid=client['client_database_id'])
                            except self.other['ts3.Error']:
                                pass
                    continue
        except Exception as er:
            return self.error(er)
