import pygame
from .platform import Platform
from src.entities.ninja import Ninja
from src.entities.heart import Heart
from src.entities.coin import Coin
from src.entities.player import Player  # Asegúrate de tener la clase Player definida

class Level3:
    def __init__(self, level_width, level_height, ninja_sprite_paths, player_sprite_paths):
        self.width = level_width
        self.height = level_height
        self.platforms = pygame.sprite.Group()
        self.ninjas = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        # Datos de plataformas: (x, y, tipo de plataforma)
        platform_data = [
            (150, level_height - 100, 1),
            (450, level_height - 250, 2),
            (800, level_height - 200, 3),
            (1200, level_height - 300, 4),
            (1600, level_height - 100, 5),
            (2000, level_height - 150, 2),
        ]

        # Crear las plataformas y añadirlas al grupo
        for x, y, platform_type in platform_data:
            platform = Platform(x, y, platform_type)
            self.platforms.add(platform)

        # Crear el jugador
        self.player = Player(100, level_height - 150, player_sprite_paths)  # Ajusta la posición inicial según sea necesario

        # Crear ninjas, corazones y monedas
        self.create_ninjas(ninja_sprite_paths)
        self.create_hearts()
        self.create_coins()

    def create_ninjas(self, sprite_paths):
        ninja_positions = [(300, self.height - 120), (900, self.height - 220), (1600, self.height - 180)]
        for pos in ninja_positions:
            ninja = Ninja(pos[0], pos[1], sprite_paths)
            self.ninjas.add(ninja)

    def reset_ninjas(self, sprite_paths):
        """Reinicia los ninjas en el nivel."""
        self.ninjas.empty()  # Eliminar todos los ninjas existentes
        self.create_ninjas(sprite_paths)  # Volver a crear los ninjas

    def create_hearts(self):
        heart_positions = [(400, self.height - 150), (1300, self.height - 250)]
        heart_images = [pygame.transform.scale(pygame.image.load(f'assets/images/heart_frame_{i}.png').convert_alpha(), (30, 30)) for i in range(3)]
        for pos in heart_positions:
            heart = Heart(pos[0], pos[1], heart_images)
            self.hearts.add(heart)

    def create_coins(self):
        coin_positions = [(200, self.height - 180), (1000, self.height - 220), (1800, self.height - 200)]
        coin_images = [pygame.transform.scale(pygame.image.load(f'assets/images/coin_frame_{i}.png').convert_alpha(), (30, 30)) for i in range(3)]
        for pos in coin_positions:
            coin = Coin(pos[0], pos[1], coin_images)
            self.coins.add(coin)

    def draw(self, screen, camera):
        for platform in self.platforms:
            screen.blit(platform.image, camera.apply(platform))
        
        for ninja in self.ninjas:
            screen.blit(ninja.image, camera.apply(ninja))
        for heart in self.hearts:
            screen.blit(heart.image, camera.apply(heart))
        for coin in self.coins:
            screen.blit(coin.image, camera.apply(coin))

    def get_platforms(self):
        return self.platforms

    def get_player(self):
        return self.player  # Método para obtener el jugador

    def reset_level(self, ninja_sprite_paths):
        """Reinicia el nivel, incluyendo el jugador y los ninjas."""
        self.player.rect.x, self.player.rect.y = 100, self.height - 150  # Reiniciar posición del jugador
        self.reset_ninjas(ninja_sprite_paths)  # Reiniciar los ninjas
        # Aquí puedes reiniciar corazones y monedas si es necesario