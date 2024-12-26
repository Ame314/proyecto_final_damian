import pygame

class Level:
    def __init__(self):
        # Crear una lista de plataformas
        self.platforms = pygame.sprite.Group()

        # Agregar plataformas (x, y, ancho, alto)
        platform_data = [
            (100, 500, 200, 20),
            (400, 400, 200, 20),
            (600, 300, 150, 20),
        ]

        for x, y, width, height in platform_data:
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)

    def draw(self, screen):
        """Dibuja todas las plataformas en la pantalla."""
        self.platforms.draw(screen)

    def get_platforms(self):
        """Devuelve las plataformas como una lista para las colisiones."""
        return self.platforms