import logging.config

import sys

from PyQt5 import QtWidgets

from gui import MainWindow
from utils import LogMessages, Variables


if __name__ == "__main__":
    logging.config.dictConfig(Variables.logger_dict)
    logger = logging.getLogger(__name__)

    logger.info(LogMessages.program_start())

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Chesscom Helper")
    window = MainWindow()
    app.exec()

    logger.info(LogMessages.program_end())
