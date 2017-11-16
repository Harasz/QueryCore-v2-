from apscheduler.schedulers.background import BackgroundScheduler


class Interval(object):

    other = {}
    S = object

    def run(self):
        return self.S.start()

    def getlibs(self, libs):
        self.S = BackgroundScheduler()
        self.other = libs
        return

    def pause(self):
        for job in self.S.get_jobs():
            job.pause()
            job.remove()
        self.S.shutdown(wait=False)
        del self.S
        return

    def resume(self):
        self.S.resume()
