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
