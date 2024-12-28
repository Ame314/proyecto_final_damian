import pygame

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.options = ["Level 1", "Level 2", "Level 3"]
        self.selected_option = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.selected_option + 1  # Retorna el nivel seleccionado

            self.screen.fill((135, 206, 250))  # Fondo azul cielo

            # Dibujar opciones del menú
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.selected_option else (0, 0, 0)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (50, 100 + i * 40))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()