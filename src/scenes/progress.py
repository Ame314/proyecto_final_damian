import pygame
import mysql.connector
from mysql.connector import Error
from src.utils.CurrentUser import CurrentUser

class ProgressScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.user_data = {}
        self.exit_button_rect = pygame.Rect(50, 500, 200, 50)  # Botón de salir
        self.menu_button_rect = pygame.Rect(300, 500, 200, 50)  # Botón de volver al menú

    def fetch_user_progress(self):
        try:
            # Conexión a la base de datos
            connection = mysql.connector.connect(
                host='172.17.0.5',
                user='root',
                password='rootpassword',
                database='game_db'
            )

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                query = """
                    SELECT 
                        u.nombre_usuario, 
                        p.nivel_alcanzado, 
                        p.puntuacion_maxima, 
                        e.tiempo_juego, 
                        e.enemigos_derrotados
                    FROM 
                        usuarios u
                    JOIN 
                        progreso p ON u.id = p.id_usuario
                    JOIN 
                        estadisticas e ON u.id = e.id_usuario
                    WHERE 
                        u.nombre_usuario = %s
                """
                cursor.execute(query, (CurrentUser.username,))
                self.user_data = cursor.fetchone() or {}
                cursor.close()
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
        finally:
            if connection.is_connected():
                connection.close()

    def run(self):
        self.fetch_user_progress()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False  # Salir de la pantalla de progreso
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        if self.exit_button_rect.collidepoint(event.pos):
                            pygame.quit()  # Salir del juego
                        elif self.menu_button_rect.collidepoint(event.pos):
                            from src.scenes.menu import MenuScreen  # Importar aquí para evitar circular import
                            return MenuScreen(self.screen)  # Volver al menú

            self.screen.fill((50, 50, 50))  # Fondo gris oscuro

            title = self.font.render("Progreso del Jugador", True, (255, 255, 255))
            self.screen.blit(title, (100, 50))

            if self.user_data:
                stats = [
                    f"Nombre de usuario: {self.user_data.get('nombre_usuario', 'N/A')}",
                    f"Nivel alcanzado: {self.user_data.get('nivel_alcanzado', 'N/A')}",
                    f"Puntuación máxima: {self.user_data.get('puntuacion_maxima', 'N/A')}",
                    f"Tiempo de juego: {self.user_data.get('tiempo_juego', 'N/A')} segundos",
                    f"Enemigos derrotados: {self.user_data.get('enemigos_derrotados', 'N/A')}",
                ]
            else:
                stats = ["No se encontraron datos para el usuario actual."]

            # Renderizar estadísticas
            for i, stat in enumerate(stats):
                text = self.font.render(stat, True, (200, 200, 200))
                self.screen.blit(text, (50, 150 + i * 40))

            # Dibujar botones
            pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button_rect)  # Botón de salir
            pygame.draw.rect(self.screen, (0, 255, 0), self.menu_button_rect)  # Botón de volver al menú

            exit_text = self.font.render("Salir", True, (255, 255, 255))
            menu_text = self.font.render("Volver al Menú", True, (255, 255, 255))
            self.screen.blit(exit_text, (self.exit_button_rect.x + 50, self.exit_button_rect.y + 10))
            self.screen.blit(menu_text, (self.menu_button_rect.x + 20, self.menu_button_rect.y + 10))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()