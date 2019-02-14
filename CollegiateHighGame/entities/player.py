import os
from math import cos, sin, radians
import pygame

from CollegiateHighGame.util.vector import Vector

DEBUG_TARGET = True


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_name, surface):
        super().__init__()

        # -- Load image -- #
        base_path = os.path.dirname(__file__)
        image_path = os.path.abspath(os.path.join(base_path, os.path.pardir))
        image_path = os.path.join(image_path, "assets", "ships", f"{sprite_name}.png")

        self.orig_image = pygame.image.load(image_path).convert_alpha()
        # self.image.set_colorkey((0, 0, 0))
        self.rect = self.orig_image.get_rect()

        size = self.orig_image.get_size()

        self.scale = 0.5

        scaled_dimensions = ((int(size[0] * self.scale)), int(size[1] * self.scale))
        self.scaled_image = pygame.transform.smoothscale(
            self.orig_image, scaled_dimensions
        )
        self.image = self.scaled_image
        self.rect = self.image.get_rect()
        # -- Load Image -- #

        self.surface = surface

        # self.x = 20
        # self.y = 20
        self.rect.center = (
            self.surface.get_rect().width / 2,
            self.surface.get_rect().height / 2,
        )

        self.max_speed = 1

        self.angle = 0

        self.position = Vector(self.rect.center)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

        if DEBUG_TARGET:
            self.target = self.rect.copy()
            self.target_radius = self.rect.width * 1.3
            self.target_angle = -90

    def update(self):
        self.velocity += self.acceleration
        # self.velocity.limit(self.max_speed)

        self.position += self.velocity
        self.acceleration = Vector(0, 0)

        self.rect.center = self.position

        if DEBUG_TARGET:
            self.target_angle += 3

            self.target.centerx = (
                cos(radians(self.target_angle)) * self.target_radius + self.rect.centerx
            )
            self.target.centery = (
                sin(radians(self.target_angle)) * self.target_radius + self.rect.centery
            )

    def draw(self):
        self.surface.blit(self.image, self.rect)

        # Debug Target
        if DEBUG_TARGET:
            pygame.draw.circle(
                self.surface,
                (255, 255, 255),
                self.rect.center,
                int(self.target_radius),
                1,
            )

            target_size = 3
            pygame.draw.circle(
                self.surface, (0, 255, 0), self.target.center, target_size
            )

    def apply_force(self, force):
        self.acceleration += Vector(force)

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle

        # orig_center = self.scaled_image.get_rect().center
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.image.get_rect().center = orig_center
