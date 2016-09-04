import threading

class OriginalThread(object):
    def __init__(self):
        self.thread_instance = threading.Thread(target=self.thread_operating)
#
    def Initialize(self):
        pass

    def Run(self):
        pass

    def ExitInstance(self):
        pass

    def Stop(self):
        pass

    def thread_operating(self):
        if self.Initialize():
            self.Run()

        self.ExitInstance()

    def launch(self):
        self.thread_instance.start()


