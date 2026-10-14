from src.game import Game
import pygame
import chess.pgn

if __name__ == "__main__":
    # Proper load of the pgn file
    with open("partie.pgn", "r", encoding="utf-8") as pgn_file:
        my_game = chess.pgn.read_game(pgn_file)
    
    # Launchs the encapsulate game
    pygame.init()
    game = Game(my_game)
    game.run()