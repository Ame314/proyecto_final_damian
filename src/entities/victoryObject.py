import pygame

class VictoryObject(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))