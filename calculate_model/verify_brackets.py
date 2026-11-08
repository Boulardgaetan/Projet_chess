import chess.pgn as pgn
import pandas as pd
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

extract_path = os.path.join(PROJECT_ROOT, "calculate_model", "extracted_games.pgn")
csv_path = os.path.join(PROJECT_ROOT, "calculate_model", "dataset.csv")

def get_elo_bracket(elo: int) -> str:
    """Determines the Elo bracket for a given rating."""
    if elo < 1600:
        return "1400-1600"
    elif elo < 1800:
        return "1600-1800"
    elif elo < 2000:
        return "1800-2000"
    elif elo < 2200:
        return "2000-2200"
    elif elo < 2400:
        return "2200-2400"
    elif elo < 2600:
        return "2400-2600"
    else:
        return "2600+"

with open(extract_path, "r", encoding="utf-8") as extracted_games:
    quotas = {
        "1400-1600": 0,
        "1600-1800": 0,
        "1800-2000": 0,
        "2000-2200": 0,
        "2200-2400": 0,
        "2400-2600": 0,
        "2600+": 0
    }
    game_count = 0

    while True:
        game = pgn.read_game(extracted_games)
        if game is None:
            print("End of PGN file reached.")
            break
                
        white_elo_str = game.headers.get("WhiteElo", "")
        black_elo_str = game.headers.get("BlackElo", "")

        # Safely parse Elo ratings (skip games with missing or invalid ratings)
        try:
            white_elo = int(white_elo_str)
            black_elo = int(black_elo_str)
        except ValueError:
            continue

        game_count += 1

        bracket_white = get_elo_bracket(white_elo)
        bracket_black = get_elo_bracket(black_elo)

        quotas[bracket_white] += 1
        quotas[bracket_black] += 1

print(f"Total processed games: {game_count}")
print("Elo brackets distribution (players count):")
print(quotas)

# Load the final dataset and sort moves by ascending Elo
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df_sorted = df.sort_values(by="Elo", ascending=True)
    df_sorted.to_csv(csv_path, index=False)
    print("Dataset successfully sorted by Elo.")
else:
    print(f"Warning: Dataset not found at {csv_path}")