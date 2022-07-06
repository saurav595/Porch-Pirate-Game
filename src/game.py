"""
Load a Tiled map file

Artwork from: https://kenney.nl
Tiled available from: https://www.mapeditor.org/

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_tiled_map
"""

import sys
import arcade
import speech_recognition as sr
import threading
import time

from player import Player
from robot import Robot
from zombie import Zombie
import AStarSearch

TILE_SCALING = 0.5
PLAYER_SCALING = 0.7

SPRITE_SCALING = 1.0
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Tiled Map Example"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 200
VIEWPORT_LEFT_MARGIN = 200

# Physics
MOVEMENT_SPEED = 3
JUMP_SPEED = 15
GRAVITY = 0.3

class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Tilemap Object
        self.tile_map = None

        # Sprite lists
        self.player_list = None
        self.enemy_list = None
        self.wall_list = None
        self.package_list = None
        self.background_list = None
        self.goal_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None

        self.physics_engine = None
        self.end_of_map = 0
        self.game_over = False

        # Cameras
        self.camera = None
        self.gui_camera = None

        # Voice command
        self.voice_recognizer = None

        # Game level difficulty
        self.level = None

    def setup(self):
        """Set up the game and initialize the variables."""

        print(self.level)

        # Player list
        self.player_list = arcade.SpriteList()

        # Enemy's list
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        # Starting position of the player
        self.player_sprite = Player(pos_x=196, pos_y=270)

        self.player_list.append(self.player_sprite)

        map_name = "map.json"
        layer_options = {
            "Platforms": {"use_spatial_hash": True},
            "Package": {"use_spatial_hash": True},
            "Background": {"use_spatial_hash": True},
            "Goal": {"use_spatial_hash": True}
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, layer_options=layer_options, scaling=TILE_SCALING
        )
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Set wall and coin SpriteLists
        self.wall_list = self.tile_map.sprite_lists["Platforms"]
        self.package_list = self.tile_map.sprite_lists["Packages"]
        self.background_list = self.tile_map.sprite_lists["Background"]
        self.goal_list = self.tile_map.sprite_lists["Goal"]

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep player from running through the wall_list layer
        walls = [self.wall_list, ]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls, gravity_constant=GRAVITY
        )

        # Create enemies and add them to the list.
        zombie = Zombie(pos_x=1200, pos_y=128, scale=SPRITE_SCALING, level=self.level)
        self.enemy_list.append(zombie)
        zombie.engine = arcade.PhysicsEnginePlatformer(zombie, self.wall_list, gravity_constant=GRAVITY/2)

        robot = Robot(pos_x=3430, pos_y=328, scale=SPRITE_SCALING, level=self.level)
        self.enemy_list.append(robot)
        robot.engine = arcade.PhysicsEnginePlatformer(robot, self.wall_list, gravity_constant=0)

        # add a physics engine to each enemy
        for e in self.enemy_list:
            #e.engine = arcade.PhysicsEnginePlatformer(e, self.wall_list, gravity_constant=GRAVITY/2)
            e.setGameInstance(self)

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Center camera on user
        self.pan_camera_to_user()

        self.game_over = False

        self.voice_recognizer = sr.Recognizer()

        # Grid size for calculations. The smaller the grid, the longer the time
        # for calculations. Make sure the grid aligns with the sprite wall grid,
        # or some openings might be missed.
        grid_size = SPRITE_SIZE

        # Calculate the playing field size. We can't generate paths outside of
        # this.
        playing_field_left_boundary = -SPRITE_SIZE * 2
        playing_field_right_boundary = SPRITE_SIZE * 35
        playing_field_top_boundary = SPRITE_SIZE * 17
        playing_field_bottom_boundary = -SPRITE_SIZE * 2

        # This calculates a list of barriers. By calculating it here in the
        # init, we are assuming this list does not change. In this example,
        # our walls don't move, so that is ok. If we want moving barriers (such as
        # moving platforms or enemies) we need to recalculate. This can be an
        # time-intensive process depending on the playing field size and grid
        # resolution.

        # Note: If the enemy sprites are the same size, we only need to calculate
        # one of these. We do NOT need a different one for each enemy. The sprite
        # is just used for a size calculation.
        self.barrier_list = AStarSearch.GameBarriers(zombie,
                                                     self.wall_list,
                                                     grid_size,
                                                     playing_field_top_boundary,
                                                     playing_field_left_boundary,
                                                     playing_field_right_boundary,
                                                     playing_field_bottom_boundary)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.camera.use()
        self.clear()

        # Draw all the sprites.
        self.background_list.draw()
        self.wall_list.draw()
        self.package_list.draw()
        self.goal_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()

        self.gui_camera.use()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(
            output, 10, 20, arcade.color.BLACK, 14
        )

        if self.game_over:
            arcade.draw_text(
                "Game Over",
                200,
                200,
                arcade.color.BLACK,
                30,
            )

        """
        for e in self.enemy_list:
            if not e.current_path is None:
                arcade.draw_line_strip(e.current_path, arcade.color.ORANGE, 1)
        """
    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        self.player_sprite.update_animation(delta_time)

        if self.player_sprite.right >= self.end_of_map:
            self.game_over = True

        # Call update on all sprites
        if not self.game_over:

             #update enemies
            self.enemy_list.update()

            # Check enemies for wall collision
            for enemy in self.enemy_list:
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                    enemy.change_y = 0

            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit an enemy. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over = True

        package_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.package_list
        )
        for package in package_hit:
            package.remove_from_sprite_lists()
            self.score += 100

        if len(arcade.check_for_collision_with_list(self.player_sprite, self.goal_list)) > 0:
            self.game_over = True

        # Pan to the user
        self.pan_camera_to_user(panning_fraction=0.50)

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """ Manage Scrolling """

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)

    def voice_command(self):

        try:
            with sr.Microphone() as source:
                audio_data = self.voice_recognizer.record(source, duration=2)
                print("Recognizing...")
                # convert speech to text
                text = self.voice_recognizer.recognize_google(audio_data)
                print(text)
                if text == "jump":
                    if self.physics_engine.can_jump():
                        self.player_sprite.change_y = JUMP_SPEED
                        self.player_sprite.change_x = 2
                        #time.sleep(1)
                        #self.player_sprite.change_x = 0
                        text = ""
                elif text == "right":
                    self.player_sprite.change_x = MOVEMENT_SPEED
                    #time.sleep(1)
                    #self.player_sprite.change_x = 0
                elif text == "left":
                    self.player_sprite.change_x = - MOVEMENT_SPEED
                    #time.sleep(1)
                    #self.player_sprite.change_x = 0
                elif text == "stop":
                    self.player_sprite.change_x = 0

        except sr.RequestError:
            print("Try again")
        except sr.UnknownValueError:
            # speech was unintelligible
            print("Try again")

    def setLevel(self, level):
        self.level = level

class SpeechRecognizerThread(threading.Thread):
    def __init__(self, threadID, game):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.game = game

    def run(self):
        time.sleep(2)
        print("Starting Speech Recognizer Thread")

        while True:
            self.game.voice_command()
            if self.game.game_over:
                break
        print("Exiting Speech Recognizer Thread")

def main():
    args = sys.argv[1:]
    print(args)
    window = MyGame()
    window.setLevel(args[1])
    window.setup()
    thread1 = SpeechRecognizerThread(1, window)
    thread1.start()
    arcade.run()

if __name__ == "__main__":
    main()