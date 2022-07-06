import arcade
import AStarSearch
import util

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)


class Enemy(arcade.Sprite):
    """An enemy sprite with basic walking movement"""

    def __init__(self, pos_x: int, pos_y: int, scale, level: str) -> None:
        super().__init__(center_x=pos_x, center_y=pos_y, scale=scale)

        self.engine = 1
        self.current_path = []
        self.path_updater_counter = 0

        # # Set up the appropriate textures
        # walking_texture_path = [
        #      ":resources:images/animated_characters/zombie/zombie_idle.png",
        #     ":resources:images/animated_characters/zombie/zombie_idle.png",
        # ]
        # standing_texture_path = ":resources:images/animated_characters/zombie/zombie_idle.png"
        #
        # # Load them all now
        # self.walk_left_textures = [
        #     arcade.load_texture(texture) for texture in walking_texture_path
        # ]
        #
        # self.walk_right_textures = [
        #     arcade.load_texture(texture, mirrored=True)
        #     for texture in walking_texture_path
        # ]
        #
        # self.stand_left_textures = [
        #     arcade.load_texture(standing_texture_path, mirrored=True)
        # ]
        # self.stand_right_textures = [
        #     arcade.load_texture(standing_texture_path)
        # ]

        # Set the enemy defaults
        self.state = arcade.FACE_LEFT
        # self.change_x = -PLAYER_MOVE_SPEED // 2

        # Set the initial texture
        # self.texture = arcade.load_texture(custom_texture)

        self.path = None

        self.playerPosition = None

        # self.width = self.width * SPRITE_SIZE
        # self.height = self.height * SPRITE_SIZE

        self.level = level

    def setGameInstance(self, gameInstance):  #: game.MyGame
        import game
        self.game = gameInstance
        print("Game instance: ")
        print(self.game)
        print("Player Sprite: ")
        print(gameInstance.player_sprite)

    def AstarPath(self):
        import game
        self.path = AStarSearch.a_star_search(self,
                                              self.game.player_sprite.position,
                                              self.game.barrier_list)
        return self.path

    def get_next_enemy_point(self):
        list = []
        list.append(self.current_path.pop(0))
        list = list + self.current_path[:1]
        self.newPosition = util.get_three_points_average(list)

    def update(self):
        super().update()

        self.path_updater_counter += 1
        self.engine.update()
        if self.path_updater_counter == 10:
            aux = self.AstarPath()
            self.path_updater_counter = 0
        else:
            aux = None

        if aux is not None:
            self.current_path = aux

        """
        if self.level == "easy":
            print("easy")
        elif self.level == "medium":
            print("medium")
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
            self.change_x = 3 * movement_direction
            attempted_jump = (self.newPosition[1] - self.position[1])
            if attempted_jump > 0:
                if self.engine.can_jump():
                    self.change_y = 3
            self.path = None
        """
        return
