from libs.LoadLib import LoadLib
from libs.Daemon import Daemon
from libs.Connect.ts3 import TS3Error
import signal
import sys


class Startbot(Daemon):

    Libs = {}
    Modules = {}

    def init(self):
        self.firstmessage()
        self.checklic()
        self.generate_licensekey()
        self.Libs = LoadLib().getmodule('libs', None)
        self.Libs['ts3.Error'] = TS3Error
        self.Libs['libs.Connect'].connect()
        self.Modules = LoadLib().getmodule('modules', self.Libs)
        signal.signal(signal.SIGINT, self.handler)

    def firstmessage(self):
        import datetime
        mess = """
                        ╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭━━━╮
                        ┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃╭━╮┃
                        ┃┃╱┃┣╮╭┳━━┳━┳╮╱╭╮┃┃╱╰╋━━┳━┳━━╮
                        ┃┃╱┃┃┃┃┃┃━┫╭┫┃╱┃┃┃┃╱╭┫╭╮┃╭┫┃━┫
                        ┃╰━╯┃╰╯┃┃━┫┃┃╰━╯┃┃╰━╯┃╰╯┃┃┃┃━┫
                        ╰━━╮┣━━┻━━┻╯╰━╮╭╯╰━━━┻━━┻╯╰━━╯
                        ╱╱╱╰╯╱╱╱╱╱╱╱╭━╯┃
                        ╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯ v2.0 By Jakubdev.me

                    © 2017{now} Jakub Sydor ALL RIGHTS RESERVED
               """

        now = datetime.datetime.now().year
        if now > 2017:
            now = '-' + str(now)
        else:
            now = ''
        print(mess.format(now=now))

    def checklic(self):
        from glob import glob
        file = '.accept'
        if glob(file):
            return
        else:
            print("""
            Przed startem aplikacji należy zaakceptować warunki licencji znajdujące się w pliku 'license.txt'.\n\n
            Czy akceptujesz warunki licencji zawarte w pliku 'license.txt' i zobowiązujesz się ich przestrzegać? (T/n):
            """)
            answer = input()
            if answer == 't' or answer == 'T':
                open(file, 'w').write('Akceptuje warunki licencji oraz zobowiązuje się ich przesatrzegać.')
            else:
                print('Warunki nie zostały zaakceptowane!')
                sys.exit(100)

    def handler(self, signum, frame):
        self.Libs['libs.Logs'].addlog('info', 'Bot kończy pracę!')
        self.Libs['libs.Connect'].close()
        return sys.exit(self.Libs['libs.Interval'].pause())

    def run(self):
        import time
        self.is_connected()
        try:
            for key, value in self.Modules.items():
                value.execute_()
                time.sleep(0.5)
            self.Libs['libs.Interval'].run()
            while True:
                self.is_connected()
                time.sleep(2)
        except Exception as er:
            self.Libs['libs.Logs'].addlog('danger', 'Bot napotkał błąd przy inicjalizacji: {}'.format(er))

    def is_connected(self):
        try:
            for key, value in self.Libs['libs.Connect'].conn.items():
                value.send_keepalive()
        except (TimeoutError, Exception):
            self.Libs['libs.Connect'].close()
            self.Libs['libs.Interval'].pause()
            self.Libs['libs.Logs'].addlog('danger', 'Utracono połączenie z serwerem!')
            self.Libs['libs.Logs'].addlog('warning', 'Nastąpi próba odzyskania połączenia')
            for key, value in self.Libs.items():
                del value
            del self.Libs
            for key, value in self.Modules.items():
                del value
            del self.Modules
            self.init()
            return self.run()
