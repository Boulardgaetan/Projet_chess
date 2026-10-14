import pygame
import sys
from chess import Board
from src.chess_analyser import ChessAnalyser,AnalysedGame
from src.gui import draw_board, draw_bar, SQUARE_SIZE
from src.parser import ExtractedGame

class Game:
    def __init__(self, my_game):
        # Initializes the fen history
        self.fen_history = []
        self.current_pos_idx = 0
        
        # Initialization of Pygame
        self.screen = pygame.display.set_mode((400+SQUARE_SIZE * 8, SQUARE_SIZE * 8))
        pygame.display.set_caption("Moteur d'Échecs - Analyseur Pro")
        self.font = pygame.font.SysFont("arial", 12, bold=True)
        self.clock = pygame.time.Clock()
        
        # Extracted Game
        self.extracted_game = ExtractedGame(my_game)
        self.fen_history = self.extracted_game.build_fen_history()
        self.board = Board(self.fen_history[0])

        # Analysed Game
        self.chess_analyser = ChessAnalyser()
        self.chess_analyser.analyse_game(self.extracted_game)
        self.analysed_game = self.chess_analyser.analysed_games[0]

    def handle_events(self):
        """Handles input to navigate through the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # Right arrow : next position
                if event.key == pygame.K_RIGHT and self.current_pos_idx < len(self.fen_history) - 1:
                    self.current_pos_idx += 1
                
                # Left arrow : precedent position
                elif event.key == pygame.K_LEFT and self.current_pos_idx > 0:
                    self.current_pos_idx -= 1
                
                # Down arrow : initial position
                elif event.key == pygame.K_DOWN:
                    self.current_pos_idx = 0
                
                # Upper arrow : Last position/Termination of the game
                elif event.key == pygame.K_UP:
                    self.current_pos_idx = len(self.fen_history) - 1

                # Instanciates the board with the right position
                self.board = Board(self.fen_history[self.current_pos_idx])

    def run(self):
        """Main loop for graphical renderer"""
        while True:
            self.handle_events()

            
            draw_board(self.screen, self.board, self.font)
            draw_bar(self.screen,self.analysed_game.winrates[self.current_pos_idx], self.analysed_game.readable_evaluation[self.current_pos_idx],self.font)
            
            pygame.display.flip()
            self.clock.tick(60)