import pygame
from src.scenes.login import LoginScreen
from src.scenes.menu import MenuScreen
from src.scenes.level import Level
from src.scenes.level2 import Level2
from src.scenes.level3 import Level3
from src.entities.player import Player
from src.utils.camara import Camera

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataformas")

# Pantalla de inicio de sesión
#login_screen = LoginScreen(screen)
#login_screen.run()

# Pantalla de menú
menu_screen = MenuScreen(screen)
selected_level = menu_screen.run()

# Dimensiones del nivel
level_width = 2400
level_height = 800

# Crear la cámara
camera = Camera(level_width, level_height, WIDTH, HEIGHT)

# Crear jugador
player = Player(100, level_height - 100, {
    'walk': 'assets/images/walk.png',
    'walk2': 'assets/images/walk2.png',
    'jumpfall': 'assets/images/jumpfall.png',
    'idle': 'assets/images/idle.png',
    'attack': 'assets/images/attack.png',
    'death': 'assets/images/death.png',  # Asegúrate de tener el sprite de muerte
    'death1': 'assets/images/death1.png'
})

# Crear el nivel seleccionado
ninja_sprite_paths = {
    'ninja_walk': 'assets/images/ninja_walk.png',
    'ninja_jumpfall': 'assets/images/ninja_jumpfall.png'
}

if selected_level == 1:
    level = Level(level_width, level_height, ninja_sprite_paths)
elif selected_level == 2:
    level = Level2(level_width, level_height, ninja_sprite_paths)
elif selected_level == 3:
    level = Level3(level_width, level_height, ninja_sprite_paths)

# Inicializar contadores
coin_count = 0
heart_count = 3
ninja_hit_time = 0

# Variables para el temporizador de muerte
death_delay_duration = 1000  # 1 segundo
death_delay_start_time = None  # Tiempo de inicio del retraso
death_delay_active = False  # Estado del retraso

# Bucle principal
clock = pygame.time.Clock()
running = True
game_over = False  # Variable para controlar el estado de juego
victory_active = False  # Variable para controlar el estado de victoria

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Verificar si el jugador ha muerto
    if heart_count <= 0:  # Si las vidas son 0
        if not death_delay_active:  # Si el retraso no está activo
            death_delay_start_time = pygame.time.get_ticks()  # Guardar el tiempo actual
            death_delay_active = True  # Activar el retraso
        else:
            # Comprobar si ha pasado el tiempo de retraso
            if pygame.time.get_ticks() - death_delay_start_time >= death_delay_duration:
                player.set_action("death1")  # Cambiar a la animación de muerte
                game_over = True  # Cambiar el estado del juego a "game over"
                death_delay_active = False  # Desactivar el retraso

    # Verificar si el jugador ha ganado
    if not game_over and not victory_active:
        for victory_object in level.victory_objects:
            if pygame.sprite.collide_rect(player, victory_object):
                victory_active = True  # Activar el estado de victoria

    if victory_active:
        screen.fill((0, 0, 0))  # Fondo negro para la pantalla de victoria
        font = pygame.font.Font(None, 36)  # Fuente más pequeña
        text = font.render("¡Has ganado!", True, (0, 255, 0))
        next_level_text = font.render("Presiona N para siguiente nivel, M para menú o ESC para salir", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(next_level_text, (WIDTH // 2 - next_level_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        # Esperar a que el jugador presione N, M o ESC
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:  # Siguiente nivel
                        # Aquí puedes cargar el siguiente nivel
                        # Por ejemplo: level = Level2(level_width, level_height, ninja_sprite_paths)
                        waiting = False
                    elif event.key == pygame.K_m:  # Volver al menú
                        selected_level = menu_screen.run()
                        if selected_level == 1:
                            level = Level(level_width, level_height, ninja_sprite_paths)
                        elif selected_level == 2:
                            level = Level2(level_width, level_height, ninja_sprite_paths)
                        elif selected_level == 3:
                            level = Level3(level_width, level_height, ninja_sprite_paths)
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:  # Salir
                        waiting = False
                        running = False
        continue  # Reiniciar el bucle para evitar que se ejecute el resto del código

    # Movimiento y animaciones
    if not game_over and not victory_active:  # Solo permitir movimiento si no está en game over y no hay victoria
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.set_action("walk_left" if keys[pygame.K_LEFT] else "walk_right")
        else:
            if not player.is_attacking and not player.is_dead:
                player.set_action("idle")

        if keys[pygame.K_SPACE]:
            player.attack()

        # Actualizar jugador
        player.update(keys, level.get_platforms(), WIDTH, HEIGHT)

        # Lógica del movimiento del Ninja
        for ninja in level.ninjas:
            ninja.update(level.get_platforms())

            # Cambiar dirección en los límites
            if ninja.facing_right:
                ninja.rect.x += 2
                if ninja.rect.right >= level_width:
                    ninja.facing_right = False
            else:
                ninja.rect.x -= 2
                if ninja.rect.left <= 0:
                    ninja.facing_right = True

            # Colisión entre jugador y ninja
            if pygame.sprite.collide_rect(player, ninja):
                if player.is_attacking:
                    ninja.take_damage()  # Llama al método para reducir la salud
                elif not player.is_dead and pygame.time.get_ticks() - ninja_hit_time > 1000:
                    heart_count -= 1
                    player.take_damage()
                    ninja_hit_time = pygame.time.get_ticks()

        # Actualizar cámara
        camera.update(player, WIDTH, HEIGHT)

        # Actualizar monedas y corazones
        level.coins.update(pygame.time.get_ticks())
        level.hearts.update(pygame.time.get_ticks())

        # Colisión jugador-monedas
        collected_coins = pygame.sprite.spritecollide(player, level.coins, True)
        coin_count += len(collected_coins)

        # Colisión jugador-corazón
        for heart in level.hearts:
            if pygame.sprite.collide_rect(player, heart):
                heart_count += 1
                heart.kill()  # Eliminar el corazón del juego

        # Dibujar todo en la pantalla
        screen.fill((135, 206, 250))  # Fondo azul cielo

        # Dibujar plataformas
        level.draw(screen, camera)

        # Dibujar monedas
        for coin in level.coins:
            screen.blit(coin.image, camera.apply(coin))

        # Dibujar jugador
        screen.blit(player.image, camera.apply(player))

        # Dibujar corazones
        for heart in level.hearts:
            screen.blit(heart.image, camera.apply(heart))

        # Dibujar contadores
        font = pygame.font.Font(None, 36)
        coin_text = font.render(f'Monedas: {coin_count}', True, (255, 255, 255))
        heart_text = font.render(f'Vidas: {heart_count}', True, (255, 255, 255))
        screen.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 10))
        screen.blit(heart_text, (WIDTH - heart_text.get_width() - 10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()