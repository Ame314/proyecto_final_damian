import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images  # Lista de imágenes para la animación
        self.index = 0  # Índice de la imagen actual
        self.image = self.images[self.index]  # Imagen inicial
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1  # Velocidad de la animación
        self.last_update = 0  # Tiempo del último cambio de imagen

    def update(self, current_time):
        # Cambiar la imagen de la moneda según el tiempo
        if current_time - self.last_update > self.animation_speed * 1000:  # Convertir a milisegundos
            self.index = (self.index + 1) % len(self.images)  # Cambiar al siguiente frame
            self.image = self.images[self.index]  # Actualizar la imagen
            self.last_update = current_time  # Actualizar el tiempo del último cambio

    def reset(self):
        self.index = 0  # Reiniciar la animación