import pygame
# clase cámara
class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)  # Usar screen_width y screen_height
        self.world_rect = pygame.Rect(0, 0, world_width, world_height)

    def apply(self, entity):
        # Aplica el desplazamiento a los sprites (especificar cómo se mueven)
        return entity.rect.move(self.camera.topleft)

    def update(self, target, width, height):
        # Ajusta la posición de la cámara para seguir al jugador
        x = -target.rect.centerx + int(width / 2)
        y = -target.rect.centery + int(height / 2)

        # Limitar los movimientos de la cámara dentro del nivel
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_rect.width - width), x)
        y = max(-(self.world_rect.height - height), y)

        self.camera = pygame.Rect(x, y, width, height)