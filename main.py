import pygame
from src.entities.player import Player
from src.scenes.level1 import Level
from src.utils.camara import Camera  # Clase Camera

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

    # Dibujar todo en la pantalla
    screen.fill((135, 206, 250))  # Fondo azul cielo
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))  # Aplicar cámara a cada sprite

    pygame.display.flip()
    clock.tick(60)

pygame.quit()