import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_paths):
        super().__init__()
        self.animations = {
            "walk_right": self.load_frames(sprite_paths['walk'], 3),
            "walk_left": self.load_frames(sprite_paths['walk2'], 3),
            "jumpfall": self.load_frames(sprite_paths['jumpfall'], 3),
            "idle": self.load_frames(sprite_paths['idle'], 4),
            "attack": self.load_frames(sprite_paths['attack'], 12),
            "death": self.load_frames(sprite_paths['death'], 9),
        }
        self.current_action = "idle"
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.facing_right = True

        self.image = self.animations[self.current_action][self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.is_attacking = False
        self.is_dead = False
        self.damage_timer = 0  # Temporizador para gestionar el daño

    def load_frames(self, sprite_sheet_path, frame_count):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = []
        sprite_width = sprite_sheet.get_width() // frame_count
        sprite_height = sprite_sheet.get_height()
        for i in range(frame_count):
            frame = sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            scaled_frame = pygame.transform.scale(frame, (60, 60))
            frames.append(scaled_frame)
        return frames

    def set_action(self, action):
        if self.current_action != action:
            self.current_action = action
            self.current_frame = 0
            self.animation_timer = 0

    def handle_platform_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    break

    def jump(self):
        if self.on_ground:
            self.velocity_y = -20
            self.on_ground = False
            self.set_action("jumpfall")

    def attack(self):
        if not self.is_attacking and not self.is_dead:
            self.is_attacking = True
            self.set_action("attack")

    def take_damage(self):
        if not self.is_dead and pygame.time.get_ticks() - self.damage_timer > 10:
            self.is_dead = True
            self.set_action("death")
            self.damage_timer = pygame.time.get_ticks()

    def update(self, keys, platforms, screen_width, screen_height):
        # Animación de muerte
        if self.is_dead:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.current_frame += 1
                if self.current_frame >= len(self.animations[self.current_action]):
                    # Finaliza la animación de muerte
                    self.is_dead = False
                    self.set_action("idle")
                self.animation_timer = 0

        # Animación de ataque
        elif self.is_attacking:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.current_frame += 1
                if self.current_frame >= len(self.animations[self.current_action]):
                    # Finaliza la animación de ataque
                    self.is_attacking = False
                    self.set_action("idle")
                self.animation_timer = 0

        # Movimiento normal
        else:
            # Movimiento horizontal
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
                self.set_action("walk_left")
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.rect.x += 5
                self.set_action("walk_right")
                self.facing_right = True
            else:
                if self.on_ground:
                    self.set_action("idle")

            # Salto
            if keys[pygame.K_UP] and self.on_ground:
                self.jump()

            # Ataque
            if keys[pygame.K_SPACE] and not self.is_attacking:
                self.attack()

        # Aplicar gravedad
        self.velocity_y += 1
        self.rect.y += self.velocity_y

        # Límite de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > screen_height:
            self.on_ground = True

        # Colisiones con plataformas
        self.handle_platform_collisions(platforms)

        # Actualizar animación
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_action])
            self.animation_timer = 0

        # Actualizar imagen
        current_image = self.animations[self.current_action][self.current_frame]
        self.image = pygame.transform.flip(current_image, True, False) if not self.facing_right else current_image
