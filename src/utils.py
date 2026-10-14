import os
import pygame

# 1. On récupère le chemin absolu de CE fichier (utils.py)
# 2. On remonte d'1 niveaux : src -> Projet échecs
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_path(*args):
    """Calcule un chemin absolu à partir de la racine du projet."""
    return os.path.join(PROJECT_ROOT, *args)

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