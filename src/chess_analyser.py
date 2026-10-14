import math
import chess
import chess.engine
from src.parser import ExtractedGame
from src.utils import get_path

class ChessAnalyser:

    def __init__(self):
        self.stockfish_path = get_path("stockfish", "stockfish.exe")
        self.analysed_games = []

    def centipoints_to_win_rate(self, cp: float) -> float:
        """Convertit un score en centipions en une probabilité de victoire (entre 0 et 1)."""
        return 1 / (1 + math.exp(-0.00368208 * cp))

    def analyse_game(self, extracted_game: ExtractedGame):
        """Analyse la partie avec Stockfish : win-rate, pertes, complexité et centipions."""
        moves_analysis = []       # Win-rate de la position (meilleur coup)
        playable_moves_count = [] # Nombre de coups viables par position
        centipoints_history = []  # Score brut en centipions (ou mat) par position
        win_rate_losses = []

        with chess.engine.SimpleEngine.popen_uci(self.stockfish_path) as engine:
            limit = chess.engine.Limit(time=0.05)  # 50ms par position
            
            for fen in extracted_game.fen_history:
                board = chess.Board(fen)
                
                # Gestion des fins de partie
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

                # On demande à Stockfish les 5 meilleurs coups (MultiPV)
                infos = engine.analyse(board, limit, multipv=5)
                
                position_win_rates = []
                best_cp = 0
                for idx, info in enumerate(infos):
                    raw_score = info["score"].white()
                    score_cp = raw_score.score(mate_score=100000)
                    
                    # On récupère le score centipion du meilleur coup (index 0)
                    if idx == 0:
                        best_cp = score_cp
                        
                    position_win_rates.append(self.centipoints_to_win_rate(score_cp))

                best_win_prob = position_win_rates[0]
                moves_analysis.append(best_win_prob)
                centipoints_history.append(best_cp)

                # Calcul du nombre de "coups jouables"
                threshold = 0.05
                good_moves = sum(1 for wp in position_win_rates if abs(wp - best_win_prob) <= threshold)
                playable_moves_count.append(good_moves)

        # Calcul des pertes de win-rate par coup
        for i in range(len(moves_analysis) - 1):
            prob_before = moves_analysis[i]
            prob_after = moves_analysis[i + 1]
            
            if i % 2 == 0:  # Blancs
                loss = prob_before - prob_after
            else:           # Noirs
                loss = prob_after - prob_before
                
            loss = max(0.0, loss)
            win_rate_losses.append(loss)

        # Calcul de qui est en train de gagner (nettoyé de l'élément en trop)
        who_is_winning = []
        for wp in moves_analysis:
            who_is_winning.append("w" if wp > 0.6 else "b" if wp < 0.4 else "equal")

        # Création de l'objet final enrichi
        analysed_game = AnalysedGame(
            extracted_game, 
            win_rate_losses, 
            playable_moves_count, 
            who_is_winning, 
            centipoints_history
        )
        self.analysed_games.append(analysed_game)


class AnalysedGame:

    def __init__(
        self, 
        game: ExtractedGame, 
        win_rate_losses: list[float], 
        playable_moves_count: list[int], 
        who_is_winning: list[str],
        centipoints_history: list[float]
    ):
        self.headers = game.headers
        self.fen_history = game.fen_history
        self.san = game.san_moves
        self.who_is_winning = who_is_winning
        self.centipoints_history = centipoints_history # <--- Stocké ici !
        
        self.win_rate_losses = win_rate_losses
        self.playable_moves_count = playable_moves_count
        
        # Séparation par joueur
        self.white_losses = win_rate_losses[0::2]
        self.black_losses = win_rate_losses[1::2]
        
        self.white_playable_counts = playable_moves_count[0::2]
        self.black_playable_counts = playable_moves_count[1::2]
        self.readable_evaluation = []
        for cp in centipoints_history:
            if abs(cp) > 90000:
                self.readable_evaluation.append(f"M{(100000 - abs(cp))}")
            else:
                self.readable_evaluation.append(f"{cp / 100:+.2f}") # Affiche par exemple "+1.50" ou "-0.30"