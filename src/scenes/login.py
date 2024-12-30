import pygame
import mysql.connector
from mysql.connector import Error
from src.scenes.menu import MenuScreen  # Importa la pantalla del menú

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.username = ""
        self.email = ""
        self.password = ""
        self.input_active = False
        self.current_input = 'email'  # Alternar entre email y password
        self.clock = pygame.time.Clock()

        # Definir los rectángulos donde se va a escribir el texto
        self.username_rect = pygame.Rect(50, 100, 300, 40)  # Campo de nombre de usuario
        self.email_rect = pygame.Rect(50, 150, 300, 40)  # Campo de email
        self.password_rect = pygame.Rect(50, 200, 300, 40)  # Campo de contraseña
        self.cursor_timer = 0  # Para controlar el parpadeo del cursor
        self.error_message = ""  # Mensaje de error

        # Botón para ir al menú
        self.menu_button_rect = pygame.Rect(50, 300, 200, 50)
        self.menu_button_text = self.font.render("Go to Menu", True, (255, 255, 255))

    def create_connection(self):
        """Crear una conexión a la base de datos."""
        connection = None
        try:
            connection = mysql.connector.connect(
                host='172.17.0.4',  # Cambia la IP o host según tu configuración
                user='root',
                password='rootpassword',
                database='game_db'
            )
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def login_user(self, email, password):
        """Verifica si el usuario existe en la base de datos."""
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        return None

    def register_user(self, username, email, password):
        """Registra un nuevo usuario en la base de datos."""
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                connection.commit()
                print(f"User {username} registered successfully!")
                return True
            except Error as e:
                print(f"The error '{e}' occurred")
            finally:
                cursor.close()
                connection.close()
        return False

    def run(self):
        running = True
        while running:
            self.error_message = ""  # Resetear mensaje de error cada ciclo

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        # Cambiar entre los campos de entrada
                        if self.current_input == 'email':
                            self.current_input = 'password'
                        elif self.current_input == 'password':
                            self.current_input = 'username'
                        else:
                            self.current_input = 'email'
                        self.input_active = True  # Activar el campo de entrada

                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            if self.email == "" or self.password == "" or self.username == "":
                                self.error_message = "All fields must be filled!"  # Mostrar error si falta información
                            elif self.current_input == 'email':
                                # Intentar hacer login
                                user = self.login_user(self.email, self.password)
                                if user:
                                    print(f"Login successful! Welcome, {user[1]}")  # Asumiendo que user[1] es el username
                                    return MenuScreen(self.screen)  # Transición al menú si el login es exitoso
                                else:
                                    self.error_message = "Login failed. Please check your credentials."  # Error de login
                            elif self.current_input == 'username':
                                # Intentar registrar usuario
                                if self.register_user(self.username, self.email, self.password):
                                    print("Registration successful! You can now log in.")
                                else:
                                    self.error_message = "Registration failed. Please try again."  # Error de registro
                        elif event.key == pygame.K_BACKSPACE:
                            if self.current_input == 'email':
                                self.email = self.email[:-1]
                            elif self.current_input == 'password':
                                self.password = self.password[:-1]
                            elif self.current_input == 'username':
                                self.username = self.username[:-1]
                        else:
                            if self.current_input == 'email':
                                self.email += event.unicode
                            elif self.current_input == 'password':
                                self.password += event.unicode  # Continuar escribiendo la contraseña
                            elif self.current_input == 'username':
                                self.username += event.unicode  # Continuar escribiendo el nombre de usuario

                # Detectar clic en el botón "Ir al menú"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button_rect.collidepoint(event.pos):
                        return MenuScreen(self.screen)  # Transición al menú cuando se hace clic en el botón

            # Dibujar fondo
            self.screen.fill((135, 206, 250))  # Fondo azul cielo

            # Fondo de los campos de entrada
            pygame.draw.rect(self.screen, (255, 255, 255), self.username_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.email_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.password_rect)

            # Dibujar los bordes de los campos de texto
            pygame.draw.rect(self.screen, (0, 0, 0), self.username_rect, 2)
            pygame.draw.rect(self.screen, (0, 0, 0), self.email_rect, 2)
            pygame.draw.rect(self.screen, (0, 0, 0), self.password_rect, 2)

            # Dibujar texto de entrada
            username_text = self.font.render(self.username, True, (0, 0, 0))
            email_text = self.font.render(self.email, True, (0, 0, 0))
            password_text = self.font.render("*" * len(self.password), True, (0, 0, 0))

            # Posicionar el texto dentro de los rectángulos
            self.screen.blit(username_text, (self.username_rect.x + 5, self.username_rect.y + 5))
            self.screen.blit(email_text, (self.email_rect.x + 5, self.email_rect.y + 5))
            self.screen.blit(password_text, (self.password_rect.x + 5, self.password_rect.y + 5))

            # Títulos de los campos
            username_label = self.font.render("Username:", True, (0, 0, 0))
            email_label = self.font.render("Email:", True, (0, 0, 0))
            password_label = self.font.render("Password:", True, (0, 0, 0))
            self.screen.blit(username_label, (50, 70))
            self.screen.blit(email_label, (50, 120))
            self.screen.blit(password_label, (50, 170))

            # Mensaje de error
            if self.error_message:
                error_text = self.font.render(self.error_message, True, (255, 0, 0))
                self.screen.blit(error_text, (50, 250))  # Mostrar mensaje de error debajo de los campos

            # Botón para ir al menú
            pygame.draw.rect(self.screen, (0, 0, 255), self.menu_button_rect)  # Botón azul
            self.screen.blit(self.menu_button_text, (self.menu_button_rect.x + 50, self.menu_button_rect.y + 10))  # Texto blanco

            # Agregar el cursor parpadeante
            if self.input_active:
                self.cursor_timer += 1
                if self.cursor_timer % 30 == 0:  # Cambiar la velocidad del parpadeo del cursor
                    cursor_position = self.username_rect if self.current_input == 'username' else self.email_rect if self.current_input == 'email' else self.password_rect
                    cursor_x = cursor_position.x + 5 + self.font.size(self.username if self.current_input == 'username' else self.email if self.current_input == 'email' else "*" * len(self.password))[0]
                    pygame.draw.line(self.screen, (0, 0, 0), (cursor_x, cursor_position.y + 5), (cursor_x, cursor_position.y + 35), 2)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
