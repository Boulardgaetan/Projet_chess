import os
import pygame

# Gets the ROOT of the project to ensure the project to compute whether the location
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_path(*args):
    """Computes the absolute path from the root of the project"""
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