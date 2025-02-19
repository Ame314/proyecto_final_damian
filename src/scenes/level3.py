import pygame
from .platform import Platform
from src.entities.ninja import Ninja
from src.entities.heart import Heart
from src.entities.coin import Coin
from src.entities.victoryObject import VictoryObject  # Asegúrate de importar la clase

class Level3:
    def __init__(self, level_width, level_height, ninja_sprite_paths):
        self.width = level_width
        self.height = level_height
        self.platforms = pygame.sprite.Group()
        self.ninjas = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.victory_objects = pygame.sprite.Group()  # Grupo para los objetos de victoria

        # Datos de plataformas: (x, y, tipo de plataforma)
        platform_data = [
            (100, level_height - 100, 1),   # First platform
            (400, level_height - 250, 2),   # Second platform, lowered for easier access
            (700, level_height - 200, 3),   # Third platform, slightly higher
            (1000, level_height - 300, 4),  # Fourth platform, lowered to create a gap
            (1400, level_height - 150, 5),  # Fifth platform, higher for a challenge
            (1800, level_height - 250, 1),  # Sixth platform, lowered for accessibility
        ]

        # Crear las plataformas y añadirlas al grupo
        for x, y, platform_type in platform_data:
            platform = Platform(x, y, platform_type, self.width)  # Pasar self.width como screen_width
            self.platforms.add(platform)

        # Añadir una plataforma en la parte inferior que cubra todo el ancho
        bottom_platform = Platform(0, level_height - 20, 6, self.width)  # Pasar self.width como screen_width
        self.platforms.add(bottom_platform)

        # Crear ninjas, corazones y monedas
        self.create_ninjas(ninja_sprite_paths)
        self.create_hearts()  # Crear 3 corazones
        self.create_coins()   # Crear 10 monedas

        # Crear el objeto de victoria al final del mapa
        self.create_victory_object()

        # Posición inicial del jugador
        self.player_start_position = (100, level_height - 150)  # Ajusta según sea necesario

    def create_victory_object(self):
        """Crea el objeto de victoria y lo añade al grupo."""
        victory_object_position = (self.width - 100, self.height - 150)  # Ajusta la posición según sea necesario
        victory_object = VictoryObject(victory_object_position[0], victory_object_position[1], 'assets/images/laba.png')  # Cambia la ruta a tu sprite
        self.victory_objects.add(victory_object)

    def get_player_start_position(self):
        return self.player_start_position  # Método para obtener la posición inicial del jugador

    def create_ninjas(self, sprite_paths):
        ninja_positions = [(200, self.height - 120), (600, self.height - 220)]
        for pos in ninja_positions:
            ninja = Ninja(pos[0], pos[1], sprite_paths)
            self.ninjas.add(ninja)

    def create_hearts(self):
        heart_positions = [
             (300, self.height - 120),  # Above the first platform
            (1000, self.height - 220), # Above the fourth platform
            (1600, self.height - 180), # Above the fifth platform
        ]  # Posiciones de los corazones
        heart_images = [pygame.transform.scale(pygame.image.load(f'assets/images/heart_frame_{i}.png').convert_alpha(), (30, 30)) for i in range(3)]
        for pos in heart_positions:
            heart = Heart(pos[0], pos[1], heart_images)
            self.hearts.add(heart)

    def create_coins(self):
        coin_positions = [
            (150, self.height - 180),  # Above the first platform
            (250, self.height - 220),  # Between the first and second platforms
            (350, self.height - 240),  # Above the second platform
            (450, self.height - 300),  # Above the second platform
            (550, self.height - 200),  # Between the second and third platforms
            (650, self.height - 150),  # Above the third platform
            (750, self.height - 250),  # Above the third platform
            (800, self.height - 300),  # Between the third and fourth platforms
            (950, self.height - 280),  # Above the fourth platform
            (1100, self.height - 220), # Above the fourth platform
            (1200, self.height - 180), # Between the fourth and fifth platforms
            (1300, self.height - 150), # Above the fifth platform
            (1450, self.height - 200), # Above the fifth platform
            (1550, self.height - 250), # Between the fifth and sixth platforms
            (1650, self.height - 180), # Above the sixth platform
            (1750, self.height - 220), # Above the sixth platform
            (1850, self.height - 500), # Between the sixth and seventh platforms
            (1900, self.height - 510), # Above the seventh platform
            (1950, self.height - 450), # Above the seventh platform
            (2000, self.height - 480), # Above the last platform
        ]
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
        for victory_object in self.victory_objects:  # Dibuja el objeto de victoria
            screen.blit(victory_object.image, camera.apply(victory_object))

    def get_platforms(self):
        return self.platforms
    
    def reset_ninjas(self, sprite_paths):
        self.ninjas.empty()  # Eliminar todos los ninjas existentes
        self.create_ninjas(sprite_paths)  # Volver a crear los ninjas

    def reset_level(self, ninja_sprite_paths):
        """Reinicia el nivel, incluyendo ninjas, corazones y monedas."""
        self.ninjas.empty()  # Eliminar todos los ninjas existentes
        self.hearts.empty()  # Eliminar todos los corazones existentes
        self.coins.empty()  # Eliminar todas las monedas existentes
        self.victory_objects.empty()  # Eliminar todos los objetos de victoria existentes

        self.create_ninjas(ninja_sprite_paths)  # Volver a crear los ninjas
        self.create_hearts()  # Volver a crear los corazones
        self.create_coins()  # Volver a crear las monedas
        self.create_victory_object()  # Volver a crear el objeto de victoria