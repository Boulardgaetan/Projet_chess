from src.game import Game
import pygame
import chess.pgn

if __name__ == "__main__":
    # Point d'entrée propre
    with open("partie.pgn", "r", encoding="utf-8") as pgn_file:
        my_game = chess.pgn.read_game(pgn_file)
    
    # Lancement du jeu encapsulé
    pygame.init()
    game = Game(my_game)
    game.run()