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
import pygame

from src.utils import global_asset_manager

# Visual configuration
SQUARE_SIZE = 80
HEIGHT = 640
WIDTH = 45
LIGHT_COLOR = (240, 217, 181)  # Cream
DARK_COLOR = (181, 136, 99)  # Brown


def draw_bar(screen, winrate, eval, font):
    """Draws the evaluation bar in the left"""
    white_height = int(winrate * HEIGHT)
    black_height = HEIGHT - white_height

    text_surface = font.render(str(eval), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 18))

    pygame.draw.rect(screen, LIGHT_COLOR, (0, black_height, WIDTH, white_height))
    pygame.draw.rect(screen, DARK_COLOR, (0, 0, WIDTH, black_height))
    screen.blit(text_surface, text_rect)


def draw_board(screen, board: chess.Board, font):
    """Draws the chessboard from the board given"""
    board_state = board.piece_map()
    sqs = SQUARE_SIZE
    for rank in range(8):
        for file in range(8):
            x = 50 + file * SQUARE_SIZE
            y = (7 - rank) * SQUARE_SIZE

            # Draws the square
            color = LIGHT_COLOR if (rank + file) % 2 == 1 else DARK_COLOR
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            # Draws the piece
            if rank * 8 + file in board_state.keys():
                piece = board_state[rank * 8 + file]
                if piece.color:
                    piece_color = "w"
                else:
                    piece_color = "b"
                type = piece_color + chess.PIECE_SYMBOLS[piece.piece_type]
                if global_asset_manager.get_image(type) is None:
                    is_white = piece.color
                    text_color = (255, 255, 255) if is_white else (20, 20, 20)

                    display_text = type

                    text_surface = font.render(display_text, True, text_color)
                    text_rect = text_surface.get_rect(
                        center=(x + sqs // 2, y + sqs // 2)
                    )
                    screen.blit(text_surface, text_rect)
                else:
                    # Loads the image from the global_asset_manager
                    raw_image = global_asset_manager.get_image(type)

                    # Rescales the image to fit the square
                    scaled_image = pygame.transform.smoothscale(raw_image, (sqs, sqs))

                    # Prints it at the right location
                    screen.blit(scaled_image, (x, y))
