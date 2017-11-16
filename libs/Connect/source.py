from libs.Connect import ts3


class ConnServer(object):

    conn = {}
    other = {}

    def getlibs(self, libs):
        self.other = libs

    def _connectinstance(self, name=''):
        import time
        i = 0
        while True:
            try:
                self.conn[name] = ts3.query.TS3Connection(
                    self.other['libs.ReadConf'].config['TS3_Connection']['Host'],
                    self.other['libs.ReadConf'].config['TS3_Connection']['Query_Port']
                                                          )
                break
            except (ConnectionRefusedError, TimeoutError, ConnectionError, Exception) as err:
                i += 1
                if i < 5:
                    self.other['libs.Logs'].addlog('danger',
                                                   'Błąd podczas próby({}) połączenia się z serwerem: {}'
                                                   '\nNastępna próba za 30 sekund'.format(i, err))
                    time.sleep(30)
                elif i < 10:
                    self.other['libs.Logs'].addlog('danger',
                                                   'Błąd podczas próby({}) połączenia się z serwerem: {}'
                                                   '\nNastępna próba za 2 minuty'.format(i, err))
                    time.sleep(120)
                else:
                    self.other['libs.Logs'].addlog('danger',
                                                   'Aplikacja nie jest w stanie nawiązać połączenia'
                                                   'z serweram. Koniec pracy.')
                    exit(10)

        self.other['libs.Logs'].addlog('',
                                       'Instancja {} uzyskała połączenie z serwerem: {}:{}'.format(
                                                name,
                                                self.other['libs.ReadConf'].config['TS3_Connection']['Host'],
                                                self.other['libs.ReadConf'].config['TS3_Connection']['Query_Port']))

        try:
            self.conn[name].login(
                client_login_name=self.other['libs.ReadConf'].config['BOT_Authentication']['Login'],
                client_login_password=self.other['libs.ReadConf'].config['BOT_Authentication']['password']
            )
        except ts3.query.TS3QueryError as err:
            self.other['libs.Logs'].addlog('danger',
                                           'Błąd podczas próby logowania z serwerem: {}'.format(err.resp.error['msg']))
            exit(4)

        self.other['libs.Logs'].addlog('info',
                                       'Zalogowano się na konto: {}'.format(
                                            self.other['libs.ReadConf'].config['BOT_Authentication']['Login']))

        try:
            self.conn[name].use(port=self.other['libs.ReadConf'].config['TS3_Connection']['Server_Port'])
            self.conn[name].clientupdate(
                client_nickname=self.other['libs.ReadConf'].config[name]['Name'] + ' (QC)'
                                   )
            if not self.other['libs.ReadConf'].config[name]['Channel_ID'] == '0':
                self.conn[name].clientmove(clid=self.conn[name].whoami()[0]['client_id'],
                                           cid=self.other['libs.ReadConf'].config[name]['Channel_ID'])
        except ts3.query.TS3QueryError as err:
            self.other['libs.Logs'].addlog('warning',
                                           'Błąd podczas ustawiania instancji {}: {}'.format(name,
                                                                                             err.resp.error['msg']))
        if self.other['libs.ReadConf'].config[name]['Event'].upper() == 'TRUE':
            try:
                self.other['libs.EventManager'].registerconn(self.conn[name], name)
            except (IndexError, ValueError, KeyError):
                self.other['libs.Logs'].addlog('warning', 'Wygląda na to, że biblioteka EventManager nie istnieje.')

        if 'libs.Database' in self.other:
            self.other['libs.Database'].add_database(name)

        self.other['libs.Logs'].addlog('', 'Ustawienia instancji {} zostały wczytane i wykonane'.format(name))

    def close(self):
        for key, value in self.conn.items():
            value.close()

    def connect(self):
        for instance in self.other['libs.ReadConf'].config.sections()[2:]:
            if self.other['libs.ReadConf'].config[instance]['Active'].upper() == 'TRUE':
                self._connectinstance(instance)
        self.other['libs.Logs'].addlog('info', 'Instancje zostały wczytane')
        self.other['libs.Logs'].addlog('info', 'Bot jest gotowy do działania!')
