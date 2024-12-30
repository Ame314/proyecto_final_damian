import pygame

class VictoryMessage:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.message = "¡Ganaste!"
        self.display_time = 4000  # Tiempo en milisegundos
        self.start_time = None
        self.active = False

    def start(self):
        """Inicia el mensaje de victoria."""
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def update(self):
        """Actualiza el estado del mensaje."""
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.display_time:
                self.active = False  # Desactiva el mensaje después del tiempo

    def draw(self):
        """Dibuja el mensaje en la pantalla."""
        if self.active:
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text_surface, text_rect)

    def is_active(self):
        """Verifica si el mensaje está activo."""
        return self.active