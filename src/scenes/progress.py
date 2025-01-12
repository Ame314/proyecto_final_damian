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
                    return  # Salir de la pantalla de progreso

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

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
