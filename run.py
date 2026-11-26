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

import chess.pgn
import pygame

from src.game import Game

if __name__ == "__main__":
    # Proper load of the pgn file
    with open("partie.pgn", encoding="utf-8") as pgn_file:
        my_game = chess.pgn.read_game(pgn_file)

    # Launchs the encapsulate game
    pygame.init()
    game = Game(my_game)
    game.run()
