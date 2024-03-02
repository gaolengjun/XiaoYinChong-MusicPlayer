from PySide6.QtCore import QThread
import work
class Play(QThread):
    def __init__(self):
        super().__init__()
        self.work = work.WorkThread()
        self.work.start()

    def dispose(self,data):
        print(data)

    def run(self):
        self.work.signal_info.connect(self.dispose)