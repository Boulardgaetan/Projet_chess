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

import math
import os

import numpy as np
import pygame

A_CLASSIC = -1147.9844030222164
B_CLASSIC = -2949.588004787255

# Computes the project root directory for absolute path resolution
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def centipoints_to_win_rate(cp: float) -> float:
    """Converts the centipawn evaluation from stockfish in win probabilities"""
    return 1 / (1 + math.exp(-0.00368208 * cp))


def get_path(*args):
    """Computes the absolute path from the root of the project"""
    return os.path.join(PROJECT_ROOT, *args)


def estimate_game_elo(moves_winrate_losses):
    """
    Estimates the ELO of the game. Returns an integer (multiple of 50) if the player's
    performance matches the model (1400-2600), else "Unclassed (< 1400)" or "2600+".
    """
    wl = np.asarray(moves_winrate_losses, dtype=float)

    # Loss mean for the moves of the game
    game_loss_mean = np.mean(wl)
    print(game_loss_mean)

    # Security for the algorithm
    if game_loss_mean <= 0:
        return "2600+"

    # Use of the logarithm formula
    brut_elo = A_CLASSIC * np.log(game_loss_mean) + B_CLASSIC

    # Rounds to the closest multiple of 50
    rounded_elo = int(round(brut_elo / 50.0) * 50)

    # Check model limits
    if rounded_elo < 1400:
        return "Unclassed (< 1400)"
    if rounded_elo > 2600:
        return "2600+"

    return rounded_elo


class AssetManager:
    def __init__(self):
        self.images = {}

    def get_image(self, name):
        if name not in self.images:
            try:
                path = get_path("assets", "images", f"{name}.png")
                image = pygame.image.load(path)
                image = image.convert_alpha()

                self.images[name] = image
            except (pygame.error, FileNotFoundError):
                return None
        return self.images[name]


global_asset_manager = AssetManager()
