import pygame

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.username = ""
        self.password = ""
        self.input_active = False
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            print(f"Username: {self.username}, Password: {self.password}")
                            # Aquí puedes agregar la lógica para verificar el inicio de sesión
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            self.username += event.unicode
                    if event.key == pygame.K_TAB:
                        self.input_active = not self.input_active

            self.screen.fill((135, 206, 250))  # Fondo azul cielo

            # Dibujar texto
            username_text = self.font.render("Username: " + self.username, True, (0, 0, 0))
            password_text = self.font.render("Password: " + "*" * len(self.password), True, (0, 0, 0))
            self.screen.blit(username_text, (50, 100))
            self.screen.blit(password_text, (50, 150))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()