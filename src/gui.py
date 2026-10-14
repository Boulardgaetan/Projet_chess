import pygame
import chess
from src.utils import global_asset_manager

# Visual configuration
SQUARE_SIZE = 80
LIGHT_COLOR = (240, 217, 181)  # Cream
DARK_COLOR = (181, 136, 99)    # Brown



def draw_board(screen, board: chess.Board, font):
    """Dessine l'échiquier et les pièces en fonction du board passé en paramètre."""
    board_state = board.piece_map()
    for rank in range(8):
        for file in range(8):
            x = file * SQUARE_SIZE
            y = (7 - rank) * SQUARE_SIZE
            
            # Draws the square
            color = LIGHT_COLOR if (rank + file) % 2 == 1 else DARK_COLOR
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            # Draws the piece
            if rank*8+file in board_state.keys():
                piece = board_state[rank*8+file]
                if piece.color:
                    piece_color = "w"
                else:
                    piece_color = "b"
                type = piece_color+chess.PIECE_SYMBOLS[piece.piece_type]
                if global_asset_manager.get_image(type) == None:
                    is_white = piece.color
                    text_color = (255, 255, 255) if is_white else (20, 20, 20)
                    
                    display_text = type
                    
                    text_surface = font.render(display_text, True, text_color)
                    text_rect = text_surface.get_rect(center=(x + SQUARE_SIZE//2, y + SQUARE_SIZE//2))
                    screen.blit(text_surface, text_rect)
                else:
                    # Loads the image from the global_asset_manager
                    raw_image = global_asset_manager.get_image(type)

                    # Rescales the image to fit the square
                    scaled_image = pygame.transform.smoothscale(raw_image, (SQUARE_SIZE, SQUARE_SIZE))

                    # Prints it at the right location
                    screen.blit(scaled_image, (x, y))