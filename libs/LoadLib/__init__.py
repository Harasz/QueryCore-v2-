import os
import glob


class LoadLib(object):

    libs = ()
    loaded = {}
    modules = []
    ignore = ('__init__.py', '__pycache__', 'disabled', 'Module',
              'Daemon', 'LoadLib', 'Main', '__init__.pyc')

    def clear(self):
        self.libs = ()
        self.loaded = {}
        self.modules = []

    def getmodule(self, dirs, libs):
        self.clear()
        last = os.getcwd()
        os.chdir(dirs)
        lib = glob.glob('*')
        try:
            for ign in self.ignore:
                if ign in lib:
                    lib.remove(ign)
        except ValueError:
            pass
        if not lib:
            raise IOError("Folder '"+dirs+"' jest pusty")
        os.chdir(last)
        return self._load(dirs, lib, libs)

    def _load(self, dirs, lib, libs):
        for mod in range(len(lib)):
            print('Ładowanie '+dirs+'.'+lib[mod], end='... ')
            self.libs += (__import__(
                                    dirs+'.'+lib[mod],
                                    globals(),
                                    locals(),
                                    lib[mod],
                                    0),
                          )
            print('Gotowe!')
        return self.initobj(libs)

    def initobj(self, other):
        for mod in range(len(self.libs)):
            if other:
                self.loaded[self.libs[mod].__name__] = self.libs[mod].Loadfile.loadobj(libs=other)
            else:
                self.loaded[self.libs[mod].__name__] = self.libs[mod].Loadfile.loadobj()
        if other:
            return self.loaded
        else:
            return self.initlib()

    def initlib(self):
        for key, value in self.loaded.items():
            value.getlibs(self.loaded)
        return self.loaded
