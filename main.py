import pygame
from src.entities.player import Player
from src.scenes.level1 import Level
from src.utils.camara import Camera  # Clase Camera
from src.entities.coin import Coin  # Clase Coin
from src.entities.heart import Heart  # Clase Heart
from src.entities.ninja import Ninja  # Clase Ninja

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataformas")

# Dimensiones del nivel
level_width = 2400
level_height = 800

# Crear la cámara
camera = Camera(level_width, level_height)

# Crear jugador
player = Player(100, level_height - 100, {
    'walk': 'assets/images/walk.png',
    'walk2': 'assets/images/walk2.png',
    'jumpfall': 'assets/images/jumpfall.png',
    'idle': 'assets/images/idle.png'
})

# Crear ninjas con diferentes posiciones
ninja_sprite_paths = {
    'ninja_walk': 'assets/images/ninja_walk.png',
    'ninja_jumpfall': 'assets/images/ninja_jumpfall.png'
}
ninjas = pygame.sprite.Group()
positions = [
    (100, level_height - 80),  # En el suelo
    (800, level_height - 320),  # En la plataforma intermedia
    (1500, level_height - 400)  # En la plataforma más alta
]

for x, y in positions:
    ninja = Ninja(x, y, ninja_sprite_paths)
    ninja.health = 1  # Agregar atributo de salud para cada ninja
    ninjas.add(ninja)

# Crear el nivel y plataformas
level = Level()

# Crear el piso
floor = pygame.sprite.Sprite()
floor.image = pygame.Surface((level_width, 20))
floor.image.fill((139, 69, 19))
floor.rect = floor.image.get_rect(topleft=(0, level_height - 20))
level.platforms.add(floor)

# Crear plataformas adicionales
platforms = [
    (400, level_height - 150, 200, 20),
    (800, level_height - 300, 200, 20),
    (1200, level_height - 200, 200, 20),
    (1600, level_height - 350, 200, 20),
    (2000, level_height - 150, 200, 20)
]

for x, y, w, h in platforms:
    platform = pygame.sprite.Sprite()
    platform.image = pygame.Surface((w, h))
    platform.image.fill((0, 128, 0))
    platform.rect = platform.image.get_rect(topleft=(x, y))
    level.platforms.add(platform)

# Crear el grupo de monedas
coin_images = [pygame.transform.scale(pygame.image.load(f'assets/images/coin_frame_{i}.png').convert_alpha(), (30, 30)) for i in range(3)]
coins = pygame.sprite.Group()
for i in range(8):
    coin = Coin(300 + i * 100, level_height - 200, coin_images)
    coins.add(coin)

# Crear el corazón
heart_images = [pygame.transform.scale(pygame.image.load(f'assets/images/heart_frame_{i}.png').convert_alpha(), (30, 30)) for i in range(3)]
heart = Heart(1000, level_height - 400, heart_images)

# Inicializar contadores
coin_count = 0
heart_count = 3
heart_collected = False
ninja_hit_time = 0  # Inicializar la variable para el manejo de colisiones

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.jump()

    # Actualizar jugador
    player.update(keys, level.get_platforms(), WIDTH, HEIGHT)

    # Lógica del movimiento del Ninja
    for ninja in ninjas:
        ninja.update(level.get_platforms())  # Actualiza posición y gravedad

        # Cambiar dirección en los límites
        if ninja.facing_right:
            ninja.rect.x += 2  # Velocidad ajustada
            if ninja.rect.right >= level_width:
                ninja.facing_right = False
        else:
            ninja.rect.x -= 2
            if ninja.rect.left <= 0:
                ninja.facing_right = True

        # Colisión entre jugador y ninja
        if pygame.sprite.collide_rect(player, ninja):
            if player.rect.bottom <= ninja.rect.top + 10 and player.velocity_y > 0:
                # Golpe desde arriba
                player.velocity_y = -10  # Rebote del jugador
                ninja.health -= 1  # Reducir salud del ninja
                if ninja.health <= 0:
                    ninja.kill()  # Eliminar al ninja si su salud es 0
            else:
                # Daño al jugador si no es un golpe válido desde arriba
                if pygame.time.get_ticks() - ninja_hit_time > 1000:  # Temporizador
                    heart_count -= 1
                    ninja_hit_time = pygame.time.get_ticks()

    # Actualizar cámara
    camera.update(player, WIDTH, HEIGHT)

    # Actualizar monedas y corazón
    coins.update(pygame.time.get_ticks())
    heart.update(pygame.time.get_ticks())

    # Colisión jugador-monedas
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    coin_count += len(collected_coins)

    # Colisión jugador-corazón
    if pygame.sprite.collide_rect(player, heart) and not heart_collected:
        heart_count += 1
        heart_collected = True
        heart.kill()

    # Dibujar elementos
    screen.fill((135, 206, 250))
    for sprite in level.platforms:
        screen.blit(sprite.image, camera.apply(sprite))
    for sprite in ninjas:
        screen.blit(sprite.image, camera.apply(sprite))
    for coin in coins:
        screen.blit(coin.image, camera.apply(coin))
    screen.blit(player.image, camera.apply(player))
    if not heart_collected:
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
