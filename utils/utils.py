import logging
import sys
from pprint import pformat

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Parser:

    @staticmethod
    def detect_player_color(soup: BeautifulSoup) -> str | None:

        # don't return if game is over
        move_divs = soup.find_all("div", "move")
        if len(move_divs) > 2:
            return ""

        # check color by looking for pieces in starting position
        w = soup.find("div", "piece wk square-51")
        b = soup.find("div", "piece wk square-58")

        if w:
            return "white"
        if b:
            return "black"
        return ""

    @staticmethod
    def parse_moves(soup: BeautifulSoup, old_moves: dict) -> dict[int, dict[str, str]]:
        """Parses html and returns a tree containing the moves.
            Example:

            {
                1: {
                    move: e4,
                    color: white
                },

                2: {
                    move: e5,
                    color: black
                },
            }

        Args:
            soup (BeautifulSoup): html
            old_moves (list): list of divs containing move info

        returns:
            dict: moves
        """
        new_moves = {}
        move_divs = soup.find_all("div", "move")

        try:
            for turn in move_divs:
                for move in turn.find_all("div"):
                    if "node" in move["class"] and not (n := int(move["data-ply"])) in old_moves:
                        new_moves[n] = {"move": move.text, "color": move["class"][0]}
                        logger.debug(f"New move: {new_moves[n]}")

        except AttributeError as e:
            logger.error(f"Could not parse moves: {e}")

        finally:
            return new_moves


class LogMessages:

    @staticmethod
    def program_start() -> str:
        return f"""
Starting Chesscom Helper on {sys.platform}
Python version {sys.version}

"""

    @staticmethod
    def program_end() -> str:
        return f"""
--------------------------------------------------------------
                      PROGRAM ENDED
--------------------------------------------------------------
"""

    @staticmethod
    def game_start(color: str) -> str:
        return f"""
--------------------------------------------------------------
                        GAME STARTED
--------------------------------------------------------------
A new game has started.
The player color is {color}
"""

    @staticmethod
    def game_end(color: str, moves: list) -> str:
        return f"""
--------------------------------------------------------------
                        GAME ENDED
--------------------------------------------------------------
The player color was {color}
The moves were:
{pformat(moves)}

 """

