# Projet Chess - Chess game analysis and performance modeling tool.
# Copyright (C) 2026  Gaëtan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import chess
import chess.pgn
from chess_detect import ChessDetector

detector = ChessDetector(lang="en", arrows=False)


class ExtractedGame:
    def __init__(self, game: chess.pgn.Game):
        self.game = game
        self.headers = self._extract_headers()
        self.fen_history = self.build_fen_history()
        self.san_moves = self.build_san_moves()
        self.long_enough = self.is_valid_for_analysis()
        self.comments = self.comment_game()
        print(self.game)

    def _extract_headers(self) -> dict[str, str]:
        """Extracts the main metadatas of the game"""
        return {
            "white": self.game.headers.get("White", "Unknown"),
            "black": self.game.headers.get("Black", "Unknown"),
            "result": self.game.headers.get("Result", "*"),
            "white_elo": self.game.headers.get("WhiteElo", "?"),
            "black_elo": self.game.headers.get("BlackElo", "?"),
            "eco": self.game.headers.get("ECO", ""),
        }

    def build_fen_history(self) -> list[str]:
        """Builds the complete fen history"""
        board = self.game.board()
        fen_history = [board.fen()]

        for move in self.game.mainline_moves():
            board.push(move)
            fen_history.append(board.fen())

        return fen_history

    def build_san_moves(self) -> list[str]:
        """Converts the main into a readable list of strings (ex: ['e4', 'e5'])."""
        board = self.game.board()
        san_list = []
        for move in self.game.mainline_moves():
            san_list.append(board.san(move))
            board.push(move)
        return san_list

    def is_valid_for_analysis(self, min_moves=10) -> bool:
        """Returns a boolean that indicates if the game is enough long for analysis"""
        return len(self.fen_history) > min_moves

    def comment_game(self):
        return detector._analyze_game(self.game)
