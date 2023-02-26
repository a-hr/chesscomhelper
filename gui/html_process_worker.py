from PyQt5 import QtCore


class HtmlProcessWorker(QtCore.QThread):
    # create a signal that will be emitted when the thread finishes
    finished = QtCore.pyqtSignal()

    def __init__(self, html: str):
        super().__init__()
        self.html = html

    def run(self):
        # parse the html here
        # emit the finished signal when done
        self.finished.emit()