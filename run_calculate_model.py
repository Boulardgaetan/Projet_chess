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

import calculate_model.from_pgn_to_data
from src.utils import get_path

GAMES_PATH = get_path("calculate_model", "games.pgn")
STOCKFISH_PATH = get_path("stockfish", "stockfish.exe")
BOOKMOVES_PATH = get_path("assets", "book_moves", "Performance.bin")
EXTRACT_PATH = get_path("calculate_model", "extracted_games.pgn")
JSON_PATH = get_path("calculate_model", "progress.json")
CSV_PATH = get_path("calculate_model", "dataset.csv")

calculate_model.from_pgn_to_data.run(
    GAMES_PATH, STOCKFISH_PATH, BOOKMOVES_PATH, EXTRACT_PATH, JSON_PATH, CSV_PATH
)
