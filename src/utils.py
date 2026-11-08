import os
import pygame
import math
import numpy as np

A_CLASSIC = -1147.9844030222164
B_CLASSIC = -2949.588004787255

# Gets the ROOT of the project to ensure the project to compute whether the location
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def centipoints_to_win_rate(cp: float) -> float:
    """Converts the centipawn evaluation from stockfish in win probabilities"""
    return 1 / (1 + math.exp(-0.00368208 * cp))

def get_path(*args):
    """Computes the absolute path from the root of the project"""
    return os.path.join(PROJECT_ROOT, *args)

def estimer_elo_partie(moves_winrate_losses):
    """
    Estime l'Elo d'une partie. Retourne un entier (multiple de 50) si le joueur 
    entre dans la plage valide (1400-2600), sinon "Non classé" ou "2600+".
    """
    wl = np.asarray(moves_winrate_losses, dtype=float)
    
    # Moyenne des pertes brutes sur l'ensemble de la partie
    perte_moyenne_partie = np.mean(wl)
    print(perte_moyenne_partie)
    
    # Sécurité pour le logarithme (pertes anormalement nulles ou négatives)
    if perte_moyenne_partie <= 0:
        return "2600+"
    
    # Application de la formule logarithmique
    elo_brut = A_CLASSIC * np.log(perte_moyenne_partie) + B_CLASSIC
    
    # Arrondi au multiple de 50 le plus proche
    elo_arrondi = int(round(elo_brut / 50.0) * 50)
    
    # Vérification des limites de validité du modèle
    if elo_arrondi < 1400:
        return "Non classé (< 1400)"
    if elo_arrondi > 2600:
        return "2600+"  # ou "Non classé (> 2600)"
        
    return elo_arrondi

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