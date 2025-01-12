import pygame
import bcrypt  # Librería para manejar contraseñas
import mysql.connector
from mysql.connector import Error
from src.scenes.menu import MenuScreen  # Importa la pantalla del menú

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 60)  # Título más grande
        self.username = ""
        self.password = ""
        self.current_input = 'username'  # Alternar entre username y password
        self.clock = pygame.time.Clock()

        # Definir los rectángulos donde se va a escribir el texto
        self.username_rect = pygame.Rect(50, 150, 300, 40)
        self.password_rect = pygame.Rect(50, 250, 300, 40)
        self.cursor_timer = 0  # Para controlar el parpadeo del cursor
        self.error_message = ""  # Mensaje de error

    def create_connection(self):
        """Crear una conexión a la base de datos."""
        try:
            connection = mysql.connector.connect(
                host='172.17.0.5',  # Cambia la IP o host según tu configuración
                user='root',
                password='rootpassword',
                database='game_db'
            )
            return connection
        except Error as e:
            print(f"The error '{e}' occurred")
            return None

    def user_exists(self, username):
        """Verifica si el usuario existe en la base de datos."""
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT nombre_usuario FROM usuarios WHERE nombre_usuario = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user is not None
        return False

    def login_user(self, username, password):
        """Verifica si el usuario existe y si la contraseña coincide."""
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT contrasena FROM usuarios WHERE nombre_usuario = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
                return True
        return False

    def register_user(self, username, password):
        """Registra un nuevo usuario en la base de datos."""
        connection = self.create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)", (username, hashed_password))
                connection.commit()
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
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        # Cambiar entre los campos de entrada
                        self.current_input = 'password' if self.current_input == 'username' else 'username'

                    elif event.key == pygame.K_RETURN:
                        if self.username == "" or self.password == "":
                            self.error_message = "Both fields must be filled!"
                        else:
                            if self.user_exists(self.username):
                                # Si el usuario existe, verificamos la contraseña
                                if self.login_user(self.username, self.password):
                                    print(f"Login successful! Welcome, {self.username}")
                                    return MenuScreen(self.screen)  # Transición al menú
                                else:
                                    self.error_message = "Incorrect password!"
                            else:
                                # Si el usuario no existe, registramos el usuario
                                print(f"Usuario no encontrado, registrando: {self.username}")
                                if self.register_user(self.username, self.password):
                                    print("Registration successful!")
                                    return MenuScreen(self.screen)  # Transición al menú
                                else:
                                    self.error_message = "Registration failed."

                    elif event.key == pygame.K_BACKSPACE:
                        if self.current_input == 'username':
                            self.username = self.username[:-1]
                        elif self.current_input == 'password':
                            self.password = self.password[:-1]
                    else:
                        if self.current_input == 'username':
                            self.username += event.unicode
                        elif self.current_input == 'password':
                            self.password += event.unicode

            # Dibujar fondo degradado suave
            self.screen.fill((173, 216, 230))  # Fondo celeste suave

            # Título centralizado
            title_text = self.title_font.render("Login / Registro", True, (0, 0, 128))
            self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, 50))

            # Dibujar los campos de texto con bordes redondeados
            pygame.draw.rect(self.screen, (255, 255, 255), self.username_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), self.password_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), self.username_rect, 2, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), self.password_rect, 2, border_radius=10)

            # Etiquetas de los campos
            username_label = self.font.render("Usuario:", True, (0, 0, 0))
            password_label = self.font.render("Contraseña:", True, (0, 0, 0))
            self.screen.blit(username_label, (self.username_rect.x, self.username_rect.y - 40))
            self.screen.blit(password_label, (self.password_rect.x, self.password_rect.y - 40))

            # Dibujar el texto ingresado
            username_text = self.font.render(self.username, True, (0, 0, 0))
            password_text = self.font.render("*" * len(self.password), True, (0, 0, 0))
            self.screen.blit(username_text, (self.username_rect.x + 5, self.username_rect.y + 5))
            self.screen.blit(password_text, (self.password_rect.x + 5, self.password_rect.y + 5))

            # Agregar cursor parpadeante
            if self.current_input == 'username' and self.cursor_timer < 15:
                pygame.draw.line(self.screen, (0, 0, 0), (self.username_rect.x + 5 + username_text.get_width(), self.username_rect.y + 5), (self.username_rect.x + 5 + username_text.get_width(), self.username_rect.y + 35), 2)
            elif self.current_input == 'password' and self.cursor_timer < 15:
                pygame.draw.line(self.screen, (0, 0, 0), (self.password_rect.x + 5 + password_text.get_width(), self.password_rect.y + 5), (self.password_rect.x + 5 + password_text.get_width(), self.password_rect.y + 35), 2)

            # Mostrar mensaje de error con fondo suave
            if self.error_message:
                error_background = pygame.Surface((self.screen.get_width(), 40))
                error_background.fill((255, 204, 204))  # Fondo rojo suave
                self.screen.blit(error_background, (0, 350))
                error_text = self.font.render(self.error_message, True, (255, 0, 0))
                self.screen.blit(error_text, (50, 355))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()