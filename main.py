import pygame
import mysql.connector
from mysql.connector import Error
from src.scenes.login import LoginScreen
from src.scenes.menu import MenuScreen
from src.scenes.progress import ProgressScreen
from src.utils.CurrentUser import CurrentUser
from src.scenes.level import Level
from src.scenes.level2 import Level2
from src.scenes.level3 import Level3
from src.entities.player import Player
from src.utils.camara import Camera

# Configuración de MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='172.17.0.5',
            user='root',
            password='rootpassword',
            database='game_db'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def save_progress(user_id, level, score, enemies_defeated, elapsed_time):
    connection = create_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        # Guardar progreso
        cursor.execute(
            """INSERT INTO progreso (id_usuario, nivel_alcanzado, puntuacion_maxima)
            VALUES (%s, %s, %s)""",
            (CurrentUser.user_id, level, score)
        )

        # Guardar estadísticas
        cursor.execute(
            """INSERT INTO estadisticas (id_usuario, tiempo_juego, enemigos_derrotados)
            VALUES (%s, %s, %s)""",
            (CurrentUser.user_id, elapsed_time, enemies_defeated) 
        )

        connection.commit()
        print("Progreso guardado correctamente.")
    except Error as e:
        print(f"Error al guardar datos: {e}")
    finally:
        connection.close()

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataformas")

# Función para mostrar la pantalla de login
def login():
    login_screen = LoginScreen(screen)
    login_screen.run()  # Aquí el usuario interactúa con la pantalla de login

# Mostrar la pantalla de login
login()

# Pantalla de menú
menu_screen = MenuScreen(screen)
selected_level = menu_screen.run()

# Dimensiones del nivel
level_width = 2400
level_height = 800

# Crear la cámara
camera = Camera(level_width, level_height, WIDTH, HEIGHT)

# Crear jugador
player_initial_x = 100
player_initial_y = level_height - 100
player = Player(player_initial_x, player_initial_y, {
    'walk': 'assets/images/walk.png',
    'walk2': 'assets/images/walk2.png',
    'jumpfall': 'assets/images/jumpfall.png',
    'idle': 'assets/images/idle.png',
    'attack': 'assets/images/attack.png',
    'death': 'assets/images/death.png',
    'death1': 'assets/images/death1.png'
})


# Crear el nivel seleccionado
ninja_sprite_paths = {
    'ninja_walk': 'assets/images/ninja_walk.png',
    'ninja_jumpfall': 'assets/images/ninja_jumpfall.png'
}

def load_level(selected_level):
    if selected_level == 1:
        return Level(level_width, level_height, ninja_sprite_paths)
    elif selected_level == 2:
        return Level2(level_width, level_height, ninja_sprite_paths)
    elif selected_level == 3:
        return Level3(level_width, level_height, ninja_sprite_paths)

level = load_level(selected_level)

# Inicialización de variables
coin_count = 0
heart_count = 3
points_count = 0
enemigos_derrotados = 0
ninja_hit_time = 0
user_id = CurrentUser.user_id  # ID del usuario en la base de datos (debería obtenerse desde el login)
victory_once = False
death_delay_duration = 1000
death_delay_start_time = None
death_delay_active = False
clock = pygame.time.Clock()
running = True
victory_active = False
game_over = False
paused = False

# Tiempo
start_time = None  # Hora en la que el nivel empieza
elapsed_time = 0  # Tiempo transcurrido

# Función para pausar el juego
def pause_menu():
    global paused, running, selected_level, level, player
    font = pygame.font.Font(None, 36)
    while paused:
        screen.fill((0, 0, 0))
        text = font.render("Juego Pausado", True, (255, 255, 255))
        resume_text = font.render("Presiona R para reanudar", True, (255, 255, 255))
        menu_text = font.render("Presiona M para ir al menú", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                elif event.key == pygame.K_m:
                    paused = False
                    selected_level = menu_screen.run()
                    level = load_level(selected_level)
                    player = Player(player_initial_x, player_initial_y, player.sprite_paths)


# Inicializar reloj y variables de estado
clock = pygame.time.Clock()
running = True
victory_active = False  # Estado de victoria
game_over = False  

start_time = pygame.time.get_ticks()
# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = True
                pause_menu()

    keys = pygame.key.get_pressed()

    # Manejo del estado de Game Over
    if heart_count <= 0 and not game_over:
        if not death_delay_active:
            death_delay_start_time = pygame.time.get_ticks()
            death_delay_active = True
        else:
            if pygame.time.get_ticks() - death_delay_start_time >= death_delay_duration:
                player.set_action("death1")
                game_over = True
                death_delay_active = False

    if game_over:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("¡Has perdido!", True, (255, 0, 0))
        restart_text = font.render("Presiona R para reiniciar, M para menú o ESC para salir", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    heart_count = 3
                    coin_count = 0
                    points_count = 0
                    player = Player(player_initial_x, player_initial_y, player.sprite_paths)
                    level = load_level(selected_level)
                elif event.key == pygame.K_m:
                    selected_level = menu_screen.run()
                    level = load_level(selected_level)
                    player = Player(player_initial_x, player_initial_y, player.sprite_paths)
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
        continue

    # Lógica de victoria
    for victory_object in level.victory_objects:
        if pygame.sprite.collide_rect(player, victory_object):
            victory_active = True

    if victory_active:
        if start_time is None:  # Iniciar el temporizador al tocar el objeto de victoria
            start_time = pygame.time.get_ticks()

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Tiempo en segundos
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("¡Has ganado!", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

        # Mostrar tiempo transcurrido
        time_text = font.render(f"Tiempo: {elapsed_time:.2f} segundos", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        pygame.time.wait(3000)  # Esperar 4 segundos
        selected_level += 1
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        save_progress(user_id, selected_level, points_count, enemigos_derrotados, elapsed_time)
        if selected_level > 3:
            screen.fill((0, 0, 0))
            text = font.render("¡Has completado el juego!", True, (0, 255, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            progress_screen = ProgressScreen(screen)  # Crear una instancia de ProgressScreen
            progress_screen.run()
            

        else:
            level = load_level(selected_level)
            player = Player(player_initial_x, player_initial_y, player.sprite_paths)
            victory_active = False
        continue

    # Lógica de movimiento y animación
    if not game_over and not victory_active:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.set_action("walk_left" if keys[pygame.K_LEFT] else "walk_right")
        else:
            if not player.is_attacking and not player.is_dead:
                player.set_action("idle")

        if keys[pygame.K_SPACE]:
            player.attack()

        player.update(keys, level.get_platforms(), WIDTH, HEIGHT)

        for ninja in level.ninjas:
            ninja.update(level.get_platforms())
            if ninja.facing_right:
                ninja.rect.x += 2
                if ninja.rect.right >= level_width:
                    ninja.facing_right = False
            else:
                ninja.rect.x -= 2
                if ninja.rect.left <= 0:
                    ninja.facing_right = True

            if pygame.sprite.collide_rect(player, ninja):
                if player.is_attacking:
                    ninja.take_damage()
                    points_count += 20
                    death_delay_active
                    enemigos_derrotados += 1 
                elif not player.is_dead and pygame.time.get_ticks() - ninja_hit_time > 1000:
                    heart_count -= 1
                    player.take_damage()
                    ninja_hit_time = pygame.time.get_ticks()

        camera.update(player, WIDTH, HEIGHT)

        level.coins.update(pygame.time.get_ticks())
        level.hearts.update(pygame.time.get_ticks())

        collected_coins = pygame.sprite.spritecollide(player, level.coins, True)
        coin_count += len(collected_coins)
        points_count += len(collected_coins)*20

        for heart in level.hearts:
            if pygame.sprite.collide_rect(player, heart):
                heart_count += 1
                points_count += 10
                heart.kill()

        screen.fill((135, 206, 250))
        level.draw(screen, camera)

        for coin in level.coins:
            screen.blit(coin.image, camera.apply(coin))

        screen.blit(player.image, camera.apply(player))

        for heart in level.hearts:
            screen.blit(heart.image, camera.apply(heart))
        
          # Mostrar el tiempo transcurrido
        time_elapsed = (pygame.time.get_ticks() - start_time) / 1000  # Tiempo en segundos
        time_text = pygame.font.Font(None, 36).render(f"Tiempo: {time_elapsed:.2f} s", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))  # Muestra el tiempo en la esquina superior izquierda

        font = pygame.font.Font(None, 36)
        coin_text = font.render(f'Monedas: {coin_count}', True, (255, 255, 255))
        heart_text = font.render(f'Vidas: {heart_count}', True, (255, 255, 255))
        points_text = font.render(f'Puntos:{points_count}',True, (255, 255, 255))
        enemy_text = font.render(f'Enemigos eliminados:{enemigos_derrotados /3}',True, (255, 255, 255))
        screen.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 10))
        screen.blit(heart_text, (WIDTH - heart_text.get_width() - 10, 50))
        screen.blit(points_text, (WIDTH - points_text.get_width() - 10, 80))
        screen.blit(enemy_text, (WIDTH - enemy_text.get_width() - 10, 100))

    pygame.display.flip()
    clock.tick(60)
# Guardar progreso al terminar
elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
save_progress(user_id, selected_level, points_count, enemigos_derrotados, elapsed_time)

pygame.quit()