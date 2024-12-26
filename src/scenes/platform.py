import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 128, 0)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)  # Color verde para las plataformas
        self.rect = self.image.get_rect(topleft=(x, y))