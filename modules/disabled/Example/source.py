from libs.Module import Module


class Example(Module):

    __name__ = 'Example'
    auto_exec = True

    def loadconf(self):
        import os
        try:
            self.config = self.other['libs.ReadConf'].loadconf('{}/module.conf'.format(
                os.path.dirname(os.path.realpath(__file__))))
        except Exception as er:
            return self.error(er)

    def execute_(self):
        return
        # Code to execute
