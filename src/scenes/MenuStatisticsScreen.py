import pygame
import mysql.connector
from mysql.connector import Error

class MenuStatisticsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 60)
        self.clock = pygame.time.Clock()
        self.statistics = self.get_statistics()

    def create_connection(self):
        """Crea una conexión a la base de datos"""
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

    def get_statistics(self):
        """Obtiene las estadísticas de la base de datos"""
        connection = self.create_connection()
        statistics = {}
        if connection:
            cursor = connection.cursor()
            # Ejemplo: Obtener el puntaje más alto y número de partidas jugadas
            cursor.execute("SELECT MAX(puntaje), COUNT(*) FROM partidas")
            result = cursor.fetchone()
            if result:
                statistics['highest_score'] = result[0] or 0  # Puntaje más alto
                statistics['games_played'] = result[1] or 0  # Partidas jugadas
            cursor.close()
            connection.close()
        return statistics

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Dibujar fondo suave
            self.screen.fill((173, 216, 230))  # Fondo celeste suave

            # Título centralizado
            title_text = self.title_font.render("Estadísticas", True, (0, 0, 128))
            self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, 50))

            # Mostrar estadísticas
            highest_score_text = self.font.render(f"Máximo puntaje: {self.statistics['highest_score']}", True, (0, 0, 0))
            games_played_text = self.font.render(f"Partidas jugadas: {self.statistics['games_played']}", True, (0, 0, 0))

            self.screen.blit(highest_score_text, (50, 150))
            self.screen.blit(games_played_text, (50, 200))

            # Agregar un botón de regreso
            back_button_text = self.font.render("Volver", True, (255, 0, 0))
            back_button_rect = back_button_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(back_button_text, back_button_rect)

            # Verificar si se hizo click en "Volver"
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and back_button_rect.collidepoint(mouse_x, mouse_y):
                running = False  # Volver a la pantalla anterior (por ejemplo, el menú principal)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
