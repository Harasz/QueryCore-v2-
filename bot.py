#!/usr/bin/env python3

if __name__ == '__main__':
    from libs.Main import Loadfile
    import sys
    import os

    os.chdir(os.path.split(__file__)[0] + '/')

    if len(sys.argv) == 2:
        Bot = Loadfile.loadobj()
        if 'start' == sys.argv[1]:
            Bot.start()
        elif 'logs' == sys.argv[1]:
            print('UWAGA! Włączono tryb logów.')
            Bot.init()
            Bot.run()
        elif 'stop' == sys.argv[1]:
            print('Bot kończy pracę.')
            Bot.stop()
        elif 'restart' == sys.argv[1]:
            print('Nastąpi restart bota.')
            Bot.restart()
        else:
            print('Nieznany argument!')
            sys.exit(0)
        sys.exit(1)
    else:
        print('Użycie: {} start | stop | logs | restart'.format(sys.argv[0]))
        sys.exit(2)
