import chess
import chess.pgn

class ExtractedGame:
    def __init__(self, game: chess.pgn.Game):
        self.game = game
        self.headers = self._extract_headers()
        self.fen_history = self.build_fen_history()
        self.san_moves = self.build_san_moves()
        self.long_enough = self.is_valid_for_analysis()

    def _extract_headers(self) -> dict[str,str]:
        """Extracts the main metadatas of the game"""
        return {
            "white": self.game.headers.get("White", "Unknown"),
            "black": self.game.headers.get("Black", "Unknown"),
            "result": self.game.headers.get("Result", "*"),
            "white_elo": self.game.headers.get("WhiteElo", "?"),
            "black_elo": self.game.headers.get("BlackElo", "?"),
            "eco": self.game.headers.get("ECO", "")
        }

    def build_fen_history(self) -> list[str]:
        """Builds the complete fen history"""
        board = self.game.board()
        fen_history = [board.fen()]
        
        for move in self.game.mainline_moves():
            board.push(move)
            fen_history.append(board.fen())
            
        return fen_history

    def build_san_moves(self) -> list[str]:
        """Converts the main into a readable list of strings (ex: ['e4', 'e5', 'Nf3'])."""
        board = self.game.board()
        san_list = []
        for move in self.game.mainline_moves():
            san_list.append(board.san(move))
            board.push(move)
        return san_list

    def is_valid_for_analysis(self, min_moves=10) -> bool:
        """Returns a boolean that indicates if the game is enough long for analysis"""
        return len(self.fen_history) > min_moves