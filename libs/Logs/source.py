import datetime


class ColorText(object):

    TEXT = '\033[{}m'
    DANGER = TEXT.format(91)
    WARNING = TEXT.format(93)
    SUCCESS = TEXT.format(92)
    INFO = TEXT.format(94)
    END = TEXT.format(0)

    def info(self, text=''):
        print(self.INFO+text+self.END)

    def succ(self, text=''):
        print(self.SUCCESS+text+self.END)

    def dang(self, text=''):
        print(self.DANGER+text+self.END)

    def warn(self, text=''):
        print(self.WARNING+text+self.END)


class Logs(ColorText):

    fileLog = (object, object)
    other = {}

    def init(self):
        self.ctrfilelog()

    def getlibs(self, libs):
        self.other = libs
        self.init()

    def ctrfilelog(self):
        self.fileLog = (
                        open('Logs/' + datetime.datetime.now().isoformat() + '.txt', 'w+'),
                        datetime.datetime.now().strftime('%d-%m-%Y'),
                       )
        self.fileLog[0].write('Logi QueryCore z dnia: {}\n'.format(self.fileLog[1]))

    def checkfilelog(self):
        date = datetime.datetime.now().strftime('%d-%m-%Y')
        if self.fileLog[1] == date:
            return True
        else:
            return self.ctrfilelog()

    def addlog(self, sing='', text='', safe=False):
        date = datetime.datetime.now()
        prefix = '[{}] '.format(date.strftime('%X'))
        text = prefix + text
        if sing == 'danger':
            self.dang(text)
            safe = True
        elif sing == 'warning':
            self.warn(text)
            safe = True
        elif sing == 'info':
            self.info(text)
        else:
            self.succ(text)

        if safe:
            self.checkfilelog()
            self.fileLog[0].write(text+'\n')
