import pygame

class Ninja(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_paths):
        super().__init__()
        self.animations = {
            "ninja_walk": self.load_frames(sprite_paths['ninja_walk'], 3),
            "ninja_jumpfall": self.load_frames(sprite_paths['ninja_jumpfall'], 4),
        }
        self.current_action = "ninja_walk"
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.facing_right = True

        self.image = self.animations[self.current_action][self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False

    def load_frames(self, sprite_sheet_path, frame_count):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = []
        sprite_width = sprite_sheet.get_width() // frame_count
        sprite_height = sprite_sheet.get_height()
        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            scaled_frame = pygame.transform.scale(frame, (60, 60))  # Ajusta el tamaño según sea necesario
            frames.append(scaled_frame)
        return frames

    def update(self, platforms):
        # Aplicar gravedad
        self.velocity_y += 1
        self.rect.y += self.velocity_y

        # Manejo de colisiones con plataformas
        self.handle_platform_collisions(platforms)

        # Animación
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_action])
            self.animation_timer = 0

        # Actualizar la imagen
        self.image = self.animations[self.current_action][self.current_frame]

    def handle_platform_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Si el ninja está cayendo
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    break

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15  # Ajusta la fuerza del salto
            self.on_ground = False
            self.current_action = "ninja_jumpfall"  # Cambiar a la animación de salto