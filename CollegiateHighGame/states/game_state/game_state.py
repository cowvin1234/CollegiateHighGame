import pygame
from pygame import locals, Vector2

# from .state import State
from CollegiateHighGame.states.state import State
from CollegiateHighGame.entities.player import Player
from CollegiateHighGame.entities.starfield import Starfield
from CollegiateHighGame.util.hash_map import HashMap
from .player_view import PlayerView

white = (255, 255, 255)


class GameState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = (29, 25, 35)
        self.divider_width = 4

        player_view1_dimensions = pygame.Rect(
            0, 0, (int(self.game.width / 2)), int(self.game.height)
        )
        player_view2_dimensions = pygame.Rect(
            self.game.width / 2, 0, (int(self.game.width / 2)), int(self.game.height)
        )

        self.player1 = Player(
            player_view1_dimensions.width / 2,
            player_view1_dimensions.height / 2,
            "playerShip1_red",
            self,
        )
        self.player2 = Player(
            player_view2_dimensions.width / 2,
            player_view2_dimensions.height / 2,
            "playerShip1_blue",
            self,
        )

        self.player1.key_mapping = {
            "up": locals.K_w,
            "down": locals.K_s,
            "left": locals.K_a,
            "right": locals.K_d,
            "shoot": locals.K_SPACE,
        }

        self.player2.key_mapping = {
            "up": locals.K_UP,
            "down": locals.K_DOWN,
            "left": locals.K_LEFT,
            "right": locals.K_RIGHT,
            "shoot": locals.K_RSHIFT,
        }

        # World State
        self.width = 6000
        self.height = 6000

        self.entities = {}
        # self.entities_spatial =
        self.cell_size = 100
        self.entities_map = HashMap(self.cell_size)

        self.entities[self.player1] = self.player1
        self.entities[self.player2] = self.player2

        player1_view_coords = (0, self.height / 2 - player_view1_dimensions.height / 2)
        player2_view_coords = (
            self.width - player_view2_dimensions.width,
            self.height / 2 - player_view2_dimensions.height / 2,
        )

        self.player1_view = PlayerView(
            surface=self.game.screen,
            dimensions=player_view1_dimensions,
            coords=player1_view_coords,
            player=self.player1,
            game=self,
            padding=(130, 130),
        )
        self.player2_view = PlayerView(
            surface=self.game.screen,
            dimensions=player_view2_dimensions,
            coords=player2_view_coords,
            player=self.player2,
            game=self,
            padding=(130, 130),
        )

        self.player1.world_pos = Vector2(self.player1_view.coords.center)
        self.player2.world_pos = Vector2(self.player2_view.coords.center)

        self.entities_map.add(self.player1, self.player1.world_pos)
        self.entities_map.add(self.player2, self.player2.world_pos)

        self.starfield = Starfield([self.player1_view, self.player2_view])
        self.starfield.prefill(10000, self.width, self.height)

    def poll_events(self, events):
        self.player1.poll_events(events)
        self.player2.poll_events(events)

    def update(self, delta_time):
        print("-----")
        for ent in list(self.entities):
            ent.update(delta_time)

            if isinstance(ent, Player):
                for item in self.entities_map.query_point(ent.world_pos):
                    if item is not ent:
                        ent.collide(item)
                        print(item, ent)
        # for key, cell in list(self.entities_map.grid.items()):
        # for ent in cell:
        # ent.update(delta_time)

        # self.player1.update()
        # self.player2.update()

        self.starfield.update(delta_time)

    def draw(self, screen):
        screen.fill(self.background)

        self.starfield.draw()

        self.player1_view.draw()
        self.player2_view.draw()

        divider = pygame.Rect(
            self.game.center_width - self.divider_width / 2,
            0,
            self.divider_width,
            self.game.height,
        )
        screen.fill(white, divider)
