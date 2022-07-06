from enemy import Enemy
import arcade

ASSETS_PATH = "../assets"
PLAYER_MOVE_SPEED = 5


class Zombie(Enemy):
    """An enemy sprite with basic walking movement"""

    def __init__(self, pos_x: int, pos_y: int, scale, level: str) -> None:
        super().__init__(pos_x=pos_x, pos_y=pos_y, scale=scale, level=level)

        self.boundary_left = pos_x - 200
        self.boundary_right = pos_x + 300
        if level == 'easy':
            self.change_x = -2.2

        # Where are the player images stored
        texture_path = ASSETS_PATH + "/" + "images" + "/" + "enemies"

        # Set up the appropriate textures
        walking_texture_path = [
            texture_path + "/zombie/character_zombie_walk0.png",
            texture_path + "/zombie/character_zombie_walk1.png",
            texture_path + "/zombie/character_zombie_walk2.png",
            texture_path + "/zombie/character_zombie_walk3.png",
            texture_path + "/zombie/character_zombie_walk4.png",
            texture_path + "/zombie/character_zombie_walk5.png",
            texture_path + "/zombie/character_zombie_walk6.png",
            texture_path + "/zombie/character_zombie_walk7.png",
        ]
        standing_texture_path = texture_path + "/" + "/zombie/character_zombie_hold.png"

        # Load them all now
        self.walk_left_textures = [
            arcade.load_texture(texture, mirrored=True)
            for texture in walking_texture_path
        ]

        self.walk_right_textures = [
            arcade.load_texture(texture, mirrored=False)
            for texture in walking_texture_path
        ]

        self.stand_left_textures = [
            arcade.load_texture(standing_texture_path)
        ]
        self.stand_right_textures = [
            arcade.load_texture(standing_texture_path)
        ]

        # Set the initial texture
        self.texture = self.stand_left_textures[0]

    def update(self):
        super().update()

        if self.level == "easy":
            if self.path_updater_counter == 0:
                if abs(self.position[0] - self.boundary_left) < 30:
                    self.change_x *= -1
                if abs(self.position[0] - self.boundary_right) < 30:
                    self.change_x *= -1

        elif self.level == "medium":
            # We pop the nex element of the enemy_path and calculate its movement trajectory
            if len(self.current_path) > 0:
                # if False:
                if (abs(self.newPosition[0] - self.position[0]) < 10) \
                        | (abs(self.newPosition[1] - self.position[1]) < 10):
                    self.get_next_enemy_point()
            else:
                self.newPosition = self.game.player_sprite.position

            movement_direction = 1 if self.newPosition[0] > self.position[0] else -1
            self.change_x = 2.0 * movement_direction
            self.path = None
        elif self.level == "hard":

            # We pop the nex element of the enemy_path and calculate its movement trajectory
            if len(self.current_path) > 0:
            #if False:
                if (abs(self.newPosition[0] - self.position[0]) < 10) \
                        | (abs(self.newPosition[1] - self.position[1]) < 10):
                    self.get_next_enemy_point()
            else:
                self.newPosition = self.game.player_sprite.position

            movement_direction = 1 if self.newPosition[0] > self.position[0] else -1
            self.change_x = 2.5 * movement_direction
            attempted_jump = (self.newPosition[1] - self.position[1])
            if attempted_jump > 0:
                if self.engine.can_jump():
                    self.change_y = 3
            self.path = None