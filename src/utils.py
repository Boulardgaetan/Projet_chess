import os
import pygame
import math

# Gets the ROOT of the project to ensure the project to compute whether the location
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def centipoints_to_win_rate(cp: float) -> float:
    """Converts the centipawn evaluation from stockfish in win probabilities"""
    return 1 / (1 + math.exp(-0.00368208 * cp))

def get_path(*args):
    """Computes the absolute path from the root of the project"""
    return os.path.join(PROJECT_ROOT, *args)

import numpy as np

A_OPT = -1175.5312750802407
B_OPT = -1631.6897211568
ALPHA_OPT = 0.1716

import numpy as np

A_OPT = -1147.9844030222164
B_OPT = -2949.588004787255

import numpy as np

A_OPT = -1147.9844030222164
B_OPT = -2949.588004787255

def estimer_elo_partie(moves_winrate_losses):
    """
    Estime l'Elo d'une partie. Retourne un entier (multiple de 50) si le joueur 
    entre dans la plage valide (1400-2600), sinon "Non classé".
    """
    wl = np.asarray(moves_winrate_losses, dtype=float)
    
    # Moyenne des pertes brutes sur l'ensemble de la partie
    perte_moyenne_partie = np.mean(wl)
    
    # Sécurité pour le logarithme (pertes anormalement nulles ou négatives)
    if perte_moyenne_partie <= 0:
        return "Non classé (> 2600)"
    
    # Application de la formule logarithmique
    elo_brut = A_OPT * np.log(perte_moyenne_partie) + B_OPT
    
    # Arrondi au multiple de 50 le plus proche
    elo_arrondi = int(round(elo_brut / 50.0) * 50)
    
    # Vérification des limites de validité du modèle
    if elo_arrondi < 1400:
        return "Non classé (< 1400)"
    if elo_arrondi > 2600:
        return "2600+"  # ou "Non classé (> 2600)"
        
    return elo_arrondi

# --- Exemple d'utilisation ---
losses_partie = [0.01, 0.04, 0.02, 0.12, 0.01]  # Donnera "Non classé (< 1400)"
resultat = estimer_elo_partie(losses_partie)
print(f"Évaluation de la partie : {resultat}")

class AssetManager:

    def __init__(self):
        self.images = {}

    def get_image(self, name):
            if name not in self.images:
                try:
                    path = get_path("assets","images", f"{name}.png")
                    image = pygame.image.load(path)
                    image = image.convert_alpha()
                        
                    self.images[name] = image
                except (pygame.error, FileNotFoundError):
                    return None
            return self.images[name]

global_asset_manager = AssetManager()