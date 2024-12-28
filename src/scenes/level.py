import pygame
from .platform import Platform

class Level:
    def __init__(self, level_width, level_height):
        self.width = level_width
        self.height = level_height
        self.platforms = pygame.sprite.Group()

        # Datos de plataformas: (x, y, tipo de plataforma)
        platform_data = [
            (100, level_height - 100, 1),  # Plataforma inicial (p1)
            (400, level_height - 200, 2),  # Plataforma media (p2)
            (700, level_height - 150, 3),  # Plataforma intermedia (p3)
            (1000, level_height - 250, 4), # Plataforma alta (p4)
            (1400, level_height - 100, 5), # Plataforma larga baja (p5)
            (1800, level_height - 300, 2), # Plataforma alta derecha (p2)
        ]

        # Crear las plataformas y añadirlas al grupo
        for x, y, platform_type in platform_data:
            platform = Platform(x, y, platform_type)
            self.platforms.add(platform)

        # Añadir una plataforma en la parte inferior que cubra todo el ancho
        bottom_platform = Platform(0, level_height - 20, 5)  # Ajusta la altura según sea necesario
        bottom_platform.rect.width = level_width  # Asegúrate de que cubra todo el ancho
        self.platforms.add(bottom_platform)

    def draw(self, screen, camera):
        # Dibuja las plataformas ajustadas a la cámara
        for platform in self.platforms:
            screen.blit(platform.image, camera.apply(platform))

    def get_platforms(self):
        return self.platforms