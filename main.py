import pygame
from src.entities.player import Player
from src.scenes.level1 import Level
from src.utils.camara import Camera  # Clase Camera
from src.entities.coin import Coin  # Asegúrate de que la clase Coin esté importada

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
player = Player(100, level_height - 120, {  # Posición inicial sobre el piso
    'walk': 'assets/images/walk.png',
    'walk2': 'assets/images/walk2.png',
    'jumpfall': 'assets/images/jumpfall.png',
    'idle': 'assets/images/idle.png'
})
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Crear el nivel y plataformas
level = Level()

# Crear el piso que cubra todo el nivel
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

# Cargar imágenes de monedas y redimensionarlas
original_coin_images = [pygame.image.load(f'assets/images/coin_frame_{i}.png').convert_alpha() for i in range(3)]
coin_images = [pygame.transform.scale(image, (30, 30)) for image in original_coin_images]  # Redimensionar a 30x30 píxeles

# Crear un grupo de monedas
coins = pygame.sprite.Group()

# Crear algunas monedas para probar
for i in range(9):  # Crear 9 monedas
    coin = Coin(300 + i * 100, level_height - 200, coin_images)  # Posiciones en la misma línea
    coins.add(coin)
    all_sprites.add(coin)  # Añadir la moneda al grupo de sprites

# Función para dibujar el contador de monedas
def draw_coin_counter(screen, count):
    font = pygame.font.Font(None, 36)  # Fuente para el contador
    text = font.render(f'Monedas: {count}', True, (255, 255, 255))  # Texto en blanco
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))  # Posición en la esquina superior derecha

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

    # Actualizar la cámara con base en el jugador
    camera.update(player, WIDTH, HEIGHT)

    # Actualizar monedas
    current_time = pygame.time.get_ticks()  # Obtener el tiempo actual
    coins.update(current_time)

    # Comprobar colisiones entre el jugador y las monedas
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    coin_count += len(collected_coins)  # Incrementar el contador de monedas

    # Dibujar todo en la pantalla
    screen.fill((135, 206, 250))  # Fondo azul cielo
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))  # Aplicar cámara a cada sprite

    # Dibujar monedas
    coins.draw(screen)

    # Dibujar el contador de monedas
    draw_coin_counter(screen, coin_count)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()