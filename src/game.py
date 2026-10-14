import pygame
import sys
from chess import Board
from src.chess_analyser import ChessAnalyser,AnalysedGame
from src.gui import draw_board, SQUARE_SIZE
from src.parser import ExtractedGame

class Game:
    def __init__(self, my_game):
        # 1. Initialisation de l'historique global
        self.fen_history = []
        self.current_pos_idx = 0
        self.current_board = None
        
        # 2. Initialisation Pygame
        self.screen = pygame.display.set_mode((SQUARE_SIZE * 8, SQUARE_SIZE * 8))
        pygame.display.set_caption("Moteur d'Échecs - Analyseur Pro")
        self.font = pygame.font.SysFont("arial", 40, bold=True)
        self.clock = pygame.time.Clock()
        
        # 3. Le jeu extrait
        self.extracted_game = ExtractedGame(my_game)
        self.fen_history = self.extracted_game.build_fen_history()
        self.board = Board(self.fen_history[0])

        # 4. Le jeu analysé
        self.chess_analyser = ChessAnalyser()
        self.chess_analyser.analyse_game(self.extracted_game)
        self.analysed_game = self.chess_analyser.analysed_games[0]
        print(self.analysed_game.readable_evaluation)

    def handle_events(self):
        """Gère les entrées clavier pour naviguer dans self.fen_history."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # Flèche Droite : Coup suivant
                if event.key == pygame.K_RIGHT and self.current_pos_idx < len(self.fen_history) - 1:
                    self.current_pos_idx += 1
                
                # Flèche Gauche : Coup précédent
                elif event.key == pygame.K_LEFT and self.current_pos_idx > 0:
                    self.current_pos_idx -= 1
                
                # 🏠 Touche Origine/Home : Revenir au début
                elif event.key == pygame.K_DOWN:
                    self.current_pos_idx = 0
                
                # Touche Fin/End : Aller au dernier coup joué
                elif event.key == pygame.K_UP:
                    self.current_pos_idx = len(self.fen_history) - 1

                # On applique la FEN de l'index actuel sur le plateau d'affichage
                self.board = Board(self.fen_history[self.current_pos_idx])

    def run(self):
        """Boucle principale de rendu graphique."""
        while True:
            self.handle_events()
            
            # On passe self.display_board à ton module de dessin passif
            draw_board(self.screen, self.board, self.font)
            
            pygame.display.flip()
            self.clock.tick(60)