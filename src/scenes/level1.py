import pygame
from .platform import Platform

class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()

        platform_data = [
            (100, 500, 200, 20),
            (400, 400, 200, 20),
            (600, 300, 150, 20),
        ]

        for x, y, width, height in platform_data:
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)

    def draw(self, screen):
        self.platforms.draw(screen)

    def get_platforms(self):
        return self.platforms
