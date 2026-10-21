import chess, chess.pgn
from src.utils import get_path
import calculate_model.from_pgn_to_data

GAMES_PATH = get_path("calculate_model","games.pgn")
STOCKFISH_PATH = get_path("stockfish", "stockfish.exe")
BOOKMOVES_PATH = get_path("assets", "book_moves", "Performance.bin")
EXTRACT_PATH = get_path("calculate_model","extracted_games.pgn")
JSON_PATH = get_path("calculate_model", "progress.json")
CSV_PATH = get_path("calculate_model", "dataset.csv")

calculate_model.from_pgn_to_data.run(GAMES_PATH,STOCKFISH_PATH,BOOKMOVES_PATH,EXTRACT_PATH, JSON_PATH, CSV_PATH)