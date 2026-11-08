import os
import pygame
import math
import chess
from utils import get_path, estimate_game_elo, centipoints_to_win_rate
from parser import ExtractedGame
import numpy as np

class ChessAnalyser:

    def __init__(self):
        self.stockfish_path = get_path("stockfish", "stockfish.exe")
        self.book_path = get_path("assets", "book_moves", "Performance.bin")
        self.analysed_games = []

    def analyse_game(self, extracted_game: ExtractedGame):
        """Analyses the game with Stockfish: win-rate, losses, complexity, and centipawns."""
        moves_analysis = [] 
        playable_moves_count = [] 
        centipoints_history = [] 
        win_rate_losses = [] 
        is_book_move_list = []

        # Simultaneous opening of engine and Polyglot book
        try:
            book_reader = chess.polyglot.open_reader(self.book_path)
        except Exception:
            book_reader = None  # Fallback safety if the path is invalid

        with chess.engine.SimpleEngine.popen_uci(self.stockfish_path) as engine:
            limit = chess.engine.Limit(depth=14)
            
            for fen in extracted_game.fen_history:
                board = chess.Board(fen)
                
                # Check if the current position is in the Polyglot book
                in_book = False
                if book_reader is not None:
                    try:
                        book_reader.find(board)
                        in_book = True
                    except IndexError:
                        in_book = False
                is_book_move_list.append(in_book)

                # Handle game endings
                if board.is_game_over():
                    if board.is_checkmate():
                        win_prob = 0.0 if board.turn == chess.WHITE else 1.0
                        cp_val = -100000 if board.turn == chess.WHITE else 100000
                    else:
                        win_prob = 0.5
                        cp_val = 0
                    
                    moves_analysis.append(win_prob)
                    playable_moves_count.append(1)
                    centipoints_history.append(cp_val)
                    continue

                # Query Stockfish for the 5 best moves (MultiPV=5)
                infos = engine.analyse(board, limit, multipv=5)
                
                position_win_rates = []
                best_cp = 0
                for idx, info in enumerate(infos):
                    raw_score = info["score"].white()
                    score_cp = raw_score.score(mate_score=100000)
                    
                    if idx == 0:
                        best_cp = score_cp
                        
                    position_win_rates.append(centipoints_to_win_rate(score_cp))

                best_win_prob = position_win_rates[0]
                moves_analysis.append(best_win_prob)
                centipoints_history.append(best_cp)

                threshold = 0.05
                good_moves = sum(1 for wp in position_win_rates if abs(wp - best_win_prob) <= threshold)
                playable_moves_count.append(good_moves)

        # Proper closure of the Polyglot book reader
        if book_reader is not None:
            book_reader.close()

        # Calculate win-rate losses per move (ignoring opening book moves)
        for i in range(len(moves_analysis) - 1):
            prob_before = moves_analysis[i]
            prob_after = moves_analysis[i + 1]
            
            # If it is a book move, set loss to 0.0
            if is_book_move_list[i]:
                loss = 0.0
            else:
                if i % 2 == 0:  # White's turn
                    loss = prob_before - prob_after
                else:           # Black's turn
                    loss = prob_after - prob_before
                loss = max(0.0, loss)
                
            win_rate_losses.append(loss)

        who_is_winning = []
        for wp in moves_analysis:
            who_is_winning.append("w" if wp > 0.6 else "b" if wp < 0.4 else "equal")

        # Store data into AnalysedGame instance
        analysed_game = AnalysedGame(
            extracted_game, 
            win_rate_losses,
            moves_analysis,
            playable_moves_count, 
            who_is_winning, 
            centipoints_history,
            is_book_move_list[1:]
        )
        self.analysed_games.append(analysed_game)
        
        # Estimate and print Elo performance for both players (for debugging/testing)
        print("Black Elo estimate:", estimate_game_elo(analysed_game.black_losses))
        print("White Elo estimate:", estimate_game_elo(analysed_game.white_losses))


class AnalysedGame:

    def __init__(
        self, 
        game: ExtractedGame, 
        win_rate_losses: list[float], 
        winrates: list[float],
        playable_moves_count: list[int], 
        who_is_winning: list[str],
        centipoints_history: list[float],
        is_book_move_list: list[bool]
    ):
        self.headers = game.headers
        self.fen_history = game.fen_history
        self.san = game.san_moves
        self.winrates = winrates
        self.who_is_winning = who_is_winning
        self.centipoints_history = centipoints_history 
        self.is_book_move = is_book_move_list
        
        self.win_rate_losses = win_rate_losses
        self.playable_moves_count = playable_moves_count
        
        # Split metrics between players
        self.white_losses = win_rate_losses[0::2]
        self.black_losses = win_rate_losses[1::2]
        
        self.white_playable_counts = playable_moves_count[0::2]
        self.black_playable_counts = playable_moves_count[1::2]
        
        self.readable_evaluation = []
        for cp in centipoints_history:
            if abs(cp) > 90000:
                mate_distance = 100000 - abs(cp)
                if mate_distance == 0:
                    self.readable_evaluation.append("1 - 0" if cp > 0 else "0 - 1")
                else:
                    self.readable_evaluation.append(f"M{mate_distance}")
            else:
                self.readable_evaluation.append(f"{cp / 100:+.2f}")