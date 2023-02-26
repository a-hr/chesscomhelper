import logging
from pathlib import Path

import chess
import chess.engine
from PyQt5 import QtCore

from utils.utils import LogMessages

logger = logging.getLogger(__name__)


class Engine(QtCore.QObject):
    recommendations = QtCore.pyqtSignal(object)
    new_move = QtCore.pyqtSignal(str)
    game_over = QtCore.pyqtSignal(str)

    def __init__(self, color: str) -> None:
        super().__init__()

        engine_path = (Path(__file__).parent / "stockfish").glob("stockfish*").__next__()
        self.engine = chess.engine.SimpleEngine.popen_uci(str(engine_path))

        self.board = chess.Board()
        self.COLOR = color

        # noinspection PyTypeChecker
        self.new_move.connect(self.add_move)

        logger.info(LogMessages.game_start(self.COLOR))

    # noinspection PyTypeChecker
    def predict(self) -> chess.engine.PlayResult:
        result = self.engine.play(
            self.board,
            chess.engine.Limit(time=0.1),
            info=chess.engine.INFO_BASIC | chess.engine.INFO_SCORE,
        )
        logger.info(f"Recommended move: {result.move}")
        self.recommendations.emit(result)

    @QtCore.pyqtSlot(str)
    def add_move(self, move: str) -> None:
        self.board.push_san(move)
        # check if game is over
        if out := self.board.outcome():
            self.game_over.emit(out.result())
            logger.info(f"Game over: {out.result()}")
            return
        logger.info(f"Added move: {move}")

    def __del__(self):
        moves = [move.uci() for move in self.board.move_stack]
        logger.info(LogMessages.game_end(self.COLOR, moves))
        self.engine.quit()
