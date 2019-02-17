import pygame
from pygame.math import Vector2

DEBUG_PADDING_LINE = True


class PlayerView:
    def __init__(self, surface, dimensions, coords, player, game, padding):
        self.dimensions = dimensions
        self.coords = pygame.Rect(
            coords[0], coords[1], dimensions.width, dimensions.height
        )
        self.surface = surface.subsurface(dimensions)
        # Make view transparent
        self.surface.fill((0, 255, 0))
        self.surface.set_colorkey((0, 255, 0))

        self.player = player
        self.game = game

        self.padding = padding
        self.padding_rect = pygame.Rect(
            padding[0],
            padding[1],
            dimensions.width - padding[0] * 2,
            dimensions.height - padding[1] * 2,
        )

        self.player.view = self

    def draw(self):
        for key, entity in self.game.world_state.entities.items():
            if key != self.player:
                offset_coords = Vector2(entity.world_pos) - Vector2(
                    self.coords.x, self.coords.y
                )
                entity.draw(self.surface, offset_coords)

        self.player.draw(self.surface)

        if DEBUG_PADDING_LINE:
            line_points = [
                self.padding_rect.topleft,
                self.padding_rect.topright,
                self.padding_rect.bottomright,
                self.padding_rect.bottomleft,
                self.padding_rect.topleft,
            ]
            pygame.draw.lines(self.surface, (255, 255, 255), True, line_points, 1)