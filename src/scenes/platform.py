import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_type, screen_width, width=None, height=20):
        super().__init__()

        # Ajustar dimensiones según el tipo de plataforma
        if platform_type == 6:
            self.width = screen_width  # La plataforma tipo 6 cubrirá todo el ancho del piso
            self.height = height  # Altura específica para la plataforma tipo 6
        else:
            self.width = width if width else 200  # Ancho predeterminado para las otras plataformas
            self.height = height  # Altura predeterminada para todas las plataformas

        # Definir las imágenes de las plataformas según el tipo
        platform_images = {
            1: "assets/images/platform1.png",
            2: "assets/images/platform1.png",
            3: "assets/images/platform1.png",
            4: "assets/images/platform2.png",
            5: "assets/images/platform2.png",
            6: None  # Nueva plataforma personalizada
        }

        # Cargar la imagen de la plataforma según el tipo
        if platform_type in platform_images and platform_images[platform_type] is not None:
            try:
                self.image = pygame.image.load(platform_images[platform_type]).convert_alpha()
            except pygame.error as e:
                raise FileNotFoundError(f"No se pudo cargar la imagen para la plataforma tipo {platform_type}: {e}")
        elif platform_type == 6:
            self.image = self.create_custom_platform()  # Crear la plataforma personalizada
        else:
            raise ValueError(f"Tipo de plataforma no válido: {platform_type}")

        # Ajustar el tamaño de la imagen para que coincida con el colisionador
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Establecer la posición de la plataforma
        self.rect = self.image.get_rect(topleft=(x, y))

    def create_custom_platform(self):
        """Crea una plataforma personalizada con un diseño de césped y tierra."""
        platform_surface = pygame.Surface((self.width, self.height))

        # Colores
        grass_color = (34, 139, 34)  # Verde (césped)
        dirt_color = (139, 69, 19)  # Café (tierra)

        # Dibujar el fondo de tierra
        platform_surface.fill(dirt_color)

        # Dibujar el césped en la parte superior
        grass_height = self.height // 2
        pygame.draw.rect(platform_surface, grass_color, (0, 0, self.width, grass_height))

        # Agregar "dientes" verdes para simular el patrón del césped
        tooth_width = 10
        tooth_height = 10
        for i in range(0, self.width, tooth_width * 2):
            pygame.draw.rect(
                platform_surface, grass_color, (i, grass_height, tooth_width, tooth_height)
            )

        return platform_surface
