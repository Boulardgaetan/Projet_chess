import json
import os
import csv
import chess
import chess.pgn
import chess.engine
import chess.polyglot
from src.utils import centipoints_to_win_rate

def get_elo_bracket(elo):
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
        return '2400-2600'
    else:
        return "2600+"

def is_game_valid(game, quotas, max_per_bracket=100, min_length=25, min_elo=1400):
    moves = list(game.mainline_moves())
    if len(moves) < min_length:
        return False
        
    white_elo_str = game.headers.get("WhiteElo")
    black_elo_str = game.headers.get("BlackElo")
    
    if not white_elo_str or not black_elo_str:
        return False
        
    try:
        white_elo = int(white_elo_str)
        black_elo = int(black_elo_str)
    except ValueError:
        return False
        
    if white_elo < min_elo or black_elo < min_elo:
        return False
        
    bracket_white = get_elo_bracket(white_elo)
    bracket_black = get_elo_bracket(black_elo)
    
    space_for_white = quotas.get(bracket_white, 0) < max_per_bracket
    space_for_black = quotas.get(bracket_black, 0) < max_per_bracket
    
    if not space_for_white and not space_for_black:
        return False
        
    if space_for_white:
        quotas[bracket_white] += 1
    if space_for_black:
        quotas[bracket_black] += 1
        
    return True

def run(games_path, stockfish_path, bookmoves_path, extract_path, json_path, csv_path):
    quotas = {
        "1400-1600": 0,
        "1600-1800": 0,
        "1800-2000": 0,
        "2000-2200": 0,
        "2200-2400": 0,
        "2400-2600": 0,
        "2600+": 0
    }
    max_per_bracket = 100
    
    start_game_count = 0
    
    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                start_game_count = data.get("last_game_count", 0)
                quotas = data.get("quotas", quotas)
                print(f"Reprise de l'extraction à partir de la partie #{start_game_count}...")
                print(f"Quotas actuels restaurés : {quotas}")
        except json.JSONDecodeError:
            print("Le fichier de progression JSON est vide ou corrompu. Reprise à la partie #0.")
            start_game_count = 0

    with open(games_path, "r", encoding="utf-8", errors="ignore") as pgn_file, \
         open(extract_path, "a", encoding="utf-8") as pgn_out, \
         open(csv_path, "a", newline="", encoding="utf-8") as csv_out:
         
        csv_writer = csv.writer(csv_out)

        file_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
        if not file_exists:
            csv_writer.writerow(["Elo", "WinRateLoss", "PlayableMovesCount"])

        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine, chess.polyglot.open_reader(bookmoves_path) as reader:
            
            game_count = 0
            
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    print("Fin du fichier PGN atteinte.")
                    break
                    
                game_count += 1
                
                if game_count <= start_game_count:
                    continue
                
                if game_count % 100 == 0:
                    print(f"Lecture en cours... {game_count} parties lues.")

                # 1. Vérification basique (longueur et plancher Elo)
                moves = list(game.mainline_moves())
                if len(moves) < 25:
                    continue
                    
                white_elo_str = game.headers.get("WhiteElo")
                black_elo_str = game.headers.get("BlackElo")
                if not white_elo_str or not black_elo_str:
                    continue
                    
                try:
                    white_elo = int(white_elo_str)
                    black_elo = int(black_elo_str)
                except ValueError:
                    continue
                    
                if white_elo < 1400 or black_elo < 1400:
                    continue
                    
                bracket_white = get_elo_bracket(white_elo)
                bracket_black = get_elo_bracket(black_elo)
                
                # Vérification des quotas sans les modifier tout de suite
                space_for_white = quotas.get(bracket_white, 0) < max_per_bracket
                space_for_black = quotas.get(bracket_black, 0) < max_per_bracket
                
                if not space_for_white and not space_for_black:
                    continue

                # --- À PARTIR D'ICI, LA PARTIE EST RETENUE ---
                
                white_elo_val = game.headers.get("WhiteElo", "?")
                black_elo_val = game.headers.get("BlackElo", "?")

                board = game.board()
                moves_analysis = []
                playable_moves_count = []
                limit = chess.engine.Limit(depth=14)

                # 2. Analyse Stockfish
                for move in game.mainline_moves():
                    is_book_move = any(entry.move == move for entry in reader.find_all(board))
                    
                    if is_book_move:
                        board.push(move)
                        continue
                        
                    if board.is_game_over():
                        if board.is_checkmate():
                            win_prob = 0.0 if board.turn == chess.WHITE else 1.0
                        else:
                            win_prob = 0.5
                        playable_moves_count.append(1)
                        moves_analysis.append(win_prob)
                        board.push(move)
                        continue

                    infos = engine.analyse(board, limit, multipv=5)
                    
                    position_win_rates = []
                    for info in infos:
                        raw_score = info["score"].white()
                        score_cp = raw_score.score(mate_score=100000)
                        position_win_rates.append(centipoints_to_win_rate(score_cp))
                    
                    best_win_prob = position_win_rates[0]
                    moves_analysis.append(best_win_prob)
                    
                    threshold = 0.05
                    good_moves = sum(1 for wp in position_win_rates if abs(wp - best_win_prob) <= threshold)
                    playable_moves_count.append(good_moves)

                    board.push(move)

                # 3. Calcul des pertes
                game_moves_data = []
                for i in range(len(moves_analysis) - 1):
                    prob_before = moves_analysis[i]
                    prob_after = moves_analysis[i + 1]
                        
                    if i % 2 == 0:  # White
                        loss = max(0.0, prob_before - prob_after)
                        game_moves_data.append((white_elo_val, loss, playable_moves_count[i]))
                    else:           # Black
                        loss = max(0.0, prob_after - prob_before)
                        game_moves_data.append((black_elo_val, loss, playable_moves_count[i]))

                # --- 4. TOUT A RÉUSSI : ON VALIDE ET ON ENREGISTRE TOUT EN MÊME TEMPS ---
                if space_for_white:
                    quotas[bracket_white] += 1
                if space_for_black:
                    quotas[bracket_black] += 1

                # Écriture dans le PGN de sortie
                exporter = chess.pgn.StringExporter(columns=80, headers=True, comments=True, variations=True)
                game_string = game.accept(exporter)
                print(game_string, file=pgn_out, end="\n\n", flush=True)

                # Écriture dans le CSV
                csv_writer.writerows(game_moves_data)
                csv_out.flush()

                # Mise à jour du fichier JSON de progression
                with open(json_path, "w", encoding="utf-8") as pf:
                    json.dump({
                        "last_game_count": game_count,
                        "quotas": quotas
                    }, pf, indent=4)
                
                if all(count >= max_per_bracket for count in quotas.values()):
                    print("Tous les quotas de tranches Elo ont été atteints !")
                    break

    print("Extraction et sauvegarde dynamique terminées avec succès !")