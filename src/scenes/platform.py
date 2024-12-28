import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_type):
        super().__init__()

        # Definir las imágenes de las plataformas según el tipo
        platform_images = {
            1: "assets/images/p1.png",
            2: "assets/images/p2.png",
            3: "assets/images/p3.png",
            4: "assets/images/p4.png",
            5: "assets/images/p5.png",
        }

        # Cargar la imagen de la plataforma según el tipo
        try:
            self.image = pygame.image.load(platform_images[platform_type]).convert_alpha()
        except KeyError:
            raise ValueError(f"Tipo de plataforma no válido: {platform_type}")
        except pygame.error as e:
            raise FileNotFoundError(f"No se pudo cargar la imagen para la plataforma tipo {platform_type}: {e}")

        # Establecer el tamaño de la plataforma
        self.width = 200  # Ancho deseado
        self.height = 20   # Altura deseada

        # Ajustar el tamaño de la imagen para que coincida con el colisionador
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Establecer la posición de la plataforma
        self.rect = self.image.get_rect(topleft=(x, y))