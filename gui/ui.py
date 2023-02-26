import logging

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from bs4 import BeautifulSoup

from utils import Variables, Parser
from engine import Engine

logger = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow):
    new_text = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.MOVES = {}
        self.COLOR = ""
        self.engine = None

        # create a web browser
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setUrl(QtCore.QUrl(Variables.url))

        # create a right side list widget
        self.list_output = QtWidgets.QListWidget()
        self.list_output.setEnabled(False)
        self.list_output.setFixedSize(200, 1080)
        self.list_output.setVerticalScrollBar(QtWidgets.QScrollBar(self))

        # add widgets to layout
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.browser)
        main_layout.addWidget(self.list_output)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # CONNECT SIGNALS
        self.browser.loadFinished.connect(self.update_title)
        Engine.recommendations.connect(self.show_text)
        Engine.game_over.connect(self.handle_end_game)
        # noinspection PyTypeChecker
        self.new_text.connect(self.show_text)

        # TIMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_html)
        self.timer.start(250)

        logger.info("GUI started!")

        self.showMaximized()
        self.show()

    def update_title(self):
        title = self.browser.page().title()
        self.browser.page().runJavaScript("console.warn = () => {};")
        self.setWindowTitle(f"{title} - ChessHelper by a-hr")

    def get_html(self):
        self.browser.page().runJavaScript(
            "document.documentElement.outerHTML", self.process_html
        )

    def process_html(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # DETECT GAME START
        if not self.COLOR:
            col = Parser.detect_player_color(soup)
            if not col:  # not in game yet
                return

            # new game starts here
            self.MOVES = {}
            self.COLOR = col
            self.engine = Engine(col)

        # CHECK FOR NEW MOVES
        new_moves = Parser.parse_moves(soup, self.MOVES)
        self.MOVES = self.MOVES | new_moves

        if not self.MOVES:
            return

        last_move = self.MOVES[len(self.MOVES)]["move"]
        self.engine.new_move.emit(last_move)

        # CHECK IF IT'S OUR TURN AND PREDICT MOVES
        if self.MOVES[len(self.MOVES)]["color"] != self.COLOR:
            # self.engine.predict()
            return

    @QtCore.pyqtSlot(list)
    def show_text(self, text_list: list[str]) -> None:
        # create a docstring for the function, explaining its use
        """
        Shows the given text on the right side list widget
        :param text_list:
        :return None:
        """
        self.list_output.clear()
        for text in text_list:
            self.list_output.addItem(text)

    @QtCore.pyqtSlot(list)
    def draw_moves(self, moves: list[str]) -> None:
        # todo: draw the moves on the board using javascript
        self.browser.page().runJavaScript(f"draw_move('{moves}')")

    @QtCore.pyqtSlot(str)
    def handle_end_game(self, result: str) -> None:
        self.MOVES = {}
        self.COLOR = ""
        self.engine = None  # kills the thread
        self.new_text.emit(["Game over!", f"Result: {result}"])

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.timer.stop()
        return super().closeEvent(a0)


# Todo: process html in a separate thread to avoid blocking the UI
# send the html to the thread and get the moves from there through a signal
# once the moves are received, send them to the engine thread through a signal
