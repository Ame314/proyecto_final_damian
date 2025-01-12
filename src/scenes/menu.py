import pygame
from src.scenes.progress import ProgressScreen

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.options = ["Level 1", "Level 2", "Level 3"]
        self.selected_option = 0

        # Botones adicionales
        self.buttons = {
            "Exit": pygame.Rect(50, 300, 150, 40),
            "Stats": pygame.Rect(50, 350, 150, 40)
        }

    def draw_buttons(self):
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (0, 128, 0), rect)
            button_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(button_text, (rect.x + 10, rect.y + 5))

    def check_button_click(self, mouse_pos):
        if self.buttons["Exit"].collidepoint(mouse_pos):
            pygame.quit()
            exit()
        elif self.buttons["Stats"].collidepoint(mouse_pos):
            self.show_stats()

    def show_stats(self):
        progress_screen = ProgressScreen(self.screen)
        progress_screen.run()

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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.check_button_click(event.pos)

            self.screen.fill((135, 206, 250))  # Fondo azul cielo

            # Dibujar opciones del menú
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.selected_option else (0, 0, 0)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (50, 100 + i * 40))

            # Dibujar botones
            self.draw_buttons()

            pygame.display.flip()
            self.clock.tick(60)

# Código principal
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Menu Example")

    # Crear una instancia de MenuScreen y llamarla
    menu = MenuScreen(screen)
    selected_level = menu.run()

    print(f"Selected Level: {selected_level}")
