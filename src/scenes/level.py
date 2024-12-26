import pygame
from .platform import Platform

class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.rocas = pygame.sprite.Group()

        # Crear el piso
        self.crear_piso()
        # Crear plataformas
        self.crear_plataformas()
        # Crear rocas
        self.crear_rocas()

    def crear_piso(self):
        # Crear el piso que cubre todo el ancho del nivel
        piso = Platform(0, 580, 2400, 20, color=(139, 69, 19))  # Color marrón
        self.platforms.add(piso)

    def crear_plataformas(self):
        # Definimos las plataformas según la descripción
        plataformas_data = [
            (100, 500, 200, 20),  # Plataforma inferior
            (100, 400, 200, 20),  # Plataforma del medio
            (100, 300, 200, 20)   # Plataforma superior
        ]

        for x, y, width, height in plataformas_data:
            plataforma = Platform(x, y, width, height)
            self.platforms.add(plataforma)

    def crear_rocas(self):
        # Crear rocas grandes
        rocas_data = [
            (600, 500, 100, 50),  # Roca grande 1
            (800, 500, 100, 50),  # Roca grande 2
            (400, 450, 50, 25)    # Roca pequeña
        ]

        for x, y, width, height in rocas_data:
            roca = Platform(x, y, width, height, color=(169, 169, 169))  # Color gris para las rocas
            self.rocas.add(roca)

    def draw(self, screen):
        self.platforms.draw(screen)
        self.rocas.draw(screen)

    def get_platforms(self):
        return self.platforms

    def get_rocas(self):
        return self.rocas