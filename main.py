import pygame
from src.entities.player import Player
from src.scenes.level1 import Level
from src.utils.camara import Camera  # Clase Camera
from src.entities.coin import Coin  # Asegúrate de que la clase Coin esté importada
from src.entities.heart import Heart  # Asegúrate de que la clase Heart esté importada
from src.entities.ninja import Ninja  # Asegúrate de que la ruta sea correcta

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataformas")

# Dimensiones del nivel
level_width = 2400  # Ancho extendido del nivel
level_height = 800  # Altura del nivel

# Crear la cámara
camera = Camera(level_width, level_height)

# Crear jugador
player = Player(100, level_height - 100, {  # Posición inicial sobre el piso
    'walk': 'assets/images/walk.png',
    'walk2': 'assets/images/walk2.png',
    'jumpfall': 'assets/images/jumpfall.png',
    'idle': 'assets/images/idle.png'
})

# Crear una instancia de Ninja
ninja_sprite_paths = {
    'ninja_walk': 'assets/images/ninja_walk.png',
    'ninja_jumpfall': 'assets/images/ninja_jumpfall.png'
}
ninja = Ninja(400, level_height - 80, ninja_sprite_paths)  # Posición inicial del ninja

all_sprites = pygame.sprite.Group()
all_sprites.add(player, ninja)

# Crear el nivel y plataformas
level = Level()

# Crear el piso que cubre todo el nivel
floor = pygame.sprite.Sprite()
floor.image = pygame.Surface((level_width, 20))
floor.image.fill((139, 69, 19))  # Color marrón
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
    platform.image.fill((0, 128, 0))  # Color verde
    platform.rect = platform.image.get_rect(topleft=(x, y))
    level.platforms.add(platform)

# Añadir plataformas al grupo de sprites
all_sprites.add(level.platforms)

# Inicializa el contador de monedas
coin_count = 0

# Inicializa el contador de corazones
heart_count = 3  # Inicializa con 3 vidas
heart_collected = False

# Variable para controlar el tiempo de espera después de tocar al ninja
ninja_hit_time = 0

# Cargar imágenes de monedas y redimensionarlas
original_coin_images = [pygame.image.load(f'assets/images/coin_frame_{i}.png').convert_alpha() for i in range(3)]
coin_images = [pygame.transform.scale(image, (30, 30)) for image in original_coin_images]  # Redimensionar a 30x30 píxeles

# Crear un grupo de monedas
coins = pygame.sprite.Group()

# Crear algunas monedas para probar
for i in range(8):  # Crear 9 monedas
    coin = Coin(300 + i * 100, level_height - 200, coin_images)  # Posiciones en la misma línea
    coins.add(coin)
    all_sprites.add(coin)  # Añadir la moneda al grupo de sprites



# Cargar imágenes de corazones y redimensionarlas
original_heart_images = [pygame.image.load(f'assets/images/heart_frame_{i}.png').convert_alpha() for i in range(3)]
heart_images = [pygame.transform.scale(image, (30, 30)) for image in original_heart_images]  # Redimensionar a 30x30 píxeles

# Crear una instancia de Heart
heart = Heart(1000, level_height - 400, heart_images)  # Posición inicial del corazón
all_sprites.add(heart)  # Añadir el corazón al grupo de sprites

# Función para dibujar el contador de monedas
def draw_coin_counter(screen, count):
    font = pygame.font.Font(None, 36)  # Fuente para el contador
    text = font.render(f'Monedas: {count}', True, (255, 255, 255))  # Texto en blanco
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))  # Posición en la esquina superior derecha

# Función para dibujar el contador de corazones
def draw_heart_counter(screen, count):
    font = pygame.font.Font(None, 36)  # Fuente para el contador
    text = font.render(f'Vidas: {count}', True, (255, 255, 255))  # Texto en blanco
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 50))  # Posición en la esquina superior derecha

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Manejar el salto
    if keys[pygame.K_SPACE]:
        player.jump()

    # Actualizar el jugador, pasando WIDTH y HEIGHT
    player.update(keys, level.get_platforms(), WIDTH, HEIGHT)

    # Asegurar que el jugador no se salga del nivel
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > level_width:
        player.rect.right = level_width

    # Movimiento del Ninja
    if ninja.rect.left <= 0 or ninja.rect.right >= level_width:
        ninja.facing_right = not ninja.facing_right  # Cambiar dirección
    ninja.move("right" if ninja.facing_right else "left")  # Mover el ninja
    ninja.update(level.get_platforms())  # Actualizar el ninja con las plataformas

    # Comprobar colisiones entre el jugador y el ninja
    if pygame.sprite.collide_rect(player, ninja):
        if player.rect.bottom <= ninja.rect.top:  # Si el jugador toca la parte superior del ninja
            ninja.kill()  # Eliminar el ninja
            ninja = Ninja(400, level_height - 80, ninja_sprite_paths)  # Reiniciar el ninja
            all_sprites.add(ninja)  # Añadir el nuevo ninja al grupo de sprites
        else:
            # Solo restar vida si no ha pasado el tiempo de espera
            if pygame.time.get_ticks() - ninja_hit_time > 1000:  # 1 segundo de delay
                heart_count -= 1  # Restar una vida al jugador
                ninja_hit_time = pygame.time.get_ticks()  # Reiniciar el tiempo de golpe

    # Actualizar la cámara con base en el jugador
    camera.update(player, WIDTH, HEIGHT)

    # Actualizar monedas
    current_time = pygame.time.get_ticks()  # Obtener el tiempo actual
    coins.update(current_time)
    heart.update(current_time)  # Actualizar la animación del corazón

    # Comprobar colisiones entre el jugador y las monedas
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    coin_count += len(collected_coins)  # Incrementar el contador de monedas

    # Comprobar colisiones entre el jugador y el corazón
    if pygame.sprite.collide_rect(player, heart) and not heart_collected:
        heart_count += 1  # Incrementar el contador de corazones
        heart_collected = True  # Marcar que el corazón ha sido recogido
        heart.kill()  # Eliminar el corazón de la pantalla

    # Dibujar todo en la pantalla
    screen.fill((135, 206, 250))  # Fondo azul cielo
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))  # Aplicar cámara a cada sprite

    # Dibujar monedas
    coins.draw(screen)

    # Dibujar el contador de monedas
    draw_coin_counter(screen, coin_count)

    # Dibujar el contador de corazones
    draw_heart_counter(screen, heart_count)

    pygame.display.flip()
    clock.tick(60)  # Ajusta la velocidad del juego aquí (60 FPS)

pygame.quit()