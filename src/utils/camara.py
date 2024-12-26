import pygame
# clase cámara

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Ajustar la posición de la entidad con base en la cámara
        return entity.rect.move(self.camera.topleft)

    def update(self, target, screen_width, screen_height):
        # Centrar la cámara en el objetivo (jugador)
        x = -target.rect.centerx + screen_width // 2
        y = -target.rect.centery + screen_height // 2

        # Limitar la cámara a los bordes del nivel
        x = min(0, x)  # No ir más a la izquierda
        x = max(-(self.width - screen_width), x)  # No ir más a la derecha
        y = min(0, y)  # No ir más arriba
        y = max(-(self.height - screen_height), y)  # No ir más abajo

        self.camera = pygame.Rect(x, y, self.width, self.height)
