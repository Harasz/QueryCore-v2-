from modules.Nickname_Checker.source import NicknameChecker


class Loadfile(object):

    def loadobj(*args, **kwargs):
        return NicknameChecker(*args, **kwargs)
