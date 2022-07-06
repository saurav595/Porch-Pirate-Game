import arcade
from enemy import Enemy

ASSETS_PATH = "../assets"
PLAYER_MOVE_SPEED = 5


class Robot(Enemy):
    """An enemy sprite with basic walking movement"""

    def __init__(self, pos_x: int, pos_y: int, scale, level: str) -> None:
        super().__init__(pos_x=pos_x, pos_y=pos_y, scale=scale, level=level)

        self.boundary_left = pos_x - 200
        self.boundary_right = pos_x + 200
        self.boundary_up = pos_y + 200

        if (level == 'easy') | (level == 'medium'):
            self.change_x = -2
            self.change_x_previous = self.change_x

        # Where are the player images stored
        texture_path = ASSETS_PATH + "/" + "images" + "/" + "enemies"

        # Set up the appropriate textures
        walking_texture_path = [
            texture_path + "/robot/character_robot_walk0.png",
            texture_path + "/robot/character_robot_walk1.png",
            texture_path + "/robot/character_robot_walk2.png",
            texture_path + "/robot/character_robot_walk3.png",
            texture_path + "/robot/character_robot_walk4.png",
            texture_path + "/robot/character_robot_walk5.png",
            texture_path + "/robot/character_robot_walk6.png",
            texture_path + "/robot/character_robot_walk7.png"
        ]
        standing_texture_path = texture_path + "/" + "/robot/character_robot_hold.png"

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
                if abs(self.position[0] - self.boundary_left) < 10:
                    self.change_x *= -1
                    self.change_y = abs(self.change_x)
                if abs(self.position[0] - self.boundary_right) < 10:
                    self.change_x *= -1
                    self.change_y = 0
                if abs(self.position[1] - self.boundary_up) < 30:
                    self.change_y *= -1
        elif self.level == "medium":
            # We start resetting the speed eliminating the extra chasing component
            x_delta = self.game.player_sprite.position[0] - self.position[0]

            if abs(x_delta) > 400:
                self.change_x = abs(self.change_x) * (1 if x_delta > 0 else -1)
            else:
                if abs(self.position[0] - self.boundary_left) < 10:
                    self.change_x *= -1
                    self.change_x_previous = self.change_x
                    self.change_y = abs(self.change_x)
                if abs(self.position[0] - self.boundary_right) < 10:
                    self.change_x *= -1
                    self.change_x_previous = self.change_x
                    self.change_y = 0
                if abs(self.position[1] - self.boundary_up) < 30:
                    self.change_y *= -1

            # We will also consider a component of movement towards the player.
            """
            if self.path_updater_counter == 0:
                self.newPosition = self.game.player_sprite.position
                distance_delta = self.newPosition[0] - self.position[0]
                if distance_delta > 0:
                    shift = min(distance_delta, self.position[0] - self.boundary_left)
                else:
                    shift = max(distance_delta, self.position[0] - self.boundary_right)
                # Update boundaries
                self.boundary_left += shift
                self.boundary_right += shift
                print(str(self.boundary_left) + "-" + str(self.boundary_right))
                """
        elif self.level == "hard":

            # We pop the nex element of the enemy_path and calculate its movement trajectory
            if len(self.current_path) > 0:
            #if False:
                if (abs(self.newPosition[0] - self.position[0]) < 10) \
                        | (abs(self.newPosition[1] - self.position[1]) < 10):
                    self.get_next_enemy_point()
            else:
                self.newPosition = self.game.player_sprite.position

            movement_direction_x = 1 if self.newPosition[0] > self.position[0] else -1
            self.change_x = 1.5 * movement_direction_x
            movement_direction_y = 1 if self.newPosition[1] > self.position[1] else -1
            self.change_y = 1.5 * movement_direction_y
            self.path = None