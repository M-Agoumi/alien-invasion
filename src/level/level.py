import time

from src.aliens.gravion import Gravion


class Level:
    def __init__(self, setting, drawer, bullets, aliens):
        """ Initialize level """
        self.pause_time = None
        self.paused_time = 0  # Total time the game has been paused
        self.time = time.time() * 1000  # get current time to calculate time passed
        self.level = 1  # first time running script level is 1
        self.scene = None  # scene to play
        self.setting = setting
        self.play = None  # current play in action
        self.drawer = drawer
        self.bullets = bullets
        self.aliens = aliens
        self.end = False

    def play_level(self):
        """ play the scene of the level """
        if self.scene is not None:
            return self.play_scene()
        else:
            return self.init_scene()

    def init_scene(self):
        """ initialize the scene of the level """
        # if self.level == 1:
        #     self.scene =
        self.parse_scene()
        return True

    def parse_scene(self):
        """ parse the scene of the level """
        self.scene = self.setting.parser.parse_level("01")

    def play_scene(self):
        """ play the scene based on time elapsed """
        # check if scene is empty and no scene is currently playing
        if not self.scene and self.play is None:
            return False
        self.play = self.get_current_event()
        """ play the current event """
        if self.end:
            return self.play_scene_end()
        if self.play:
            print(self.play)
            if self.play['type'] == 'message':
                self.play_scene_message()
            elif self.play['type'] == 'spawn':
                self.play_spawn()
            elif self.play['type'] == 'end':
                self.end = True

        return True

    def get_current_event(self):
        """ get the current event to play """
        if not self.scene:
            return False

        # get current time
        current_time = time.time() * 1000

        # Calculate time elapsed, considering paused time
        time_elapsed = current_time - self.time - self.paused_time

        # get current event
        current_event = self.scene[0]

        # get event time
        event_time = current_event["timestamp"]

        # if time elapsed is greater than event time
        if time_elapsed > event_time:
            # remove event from scene
            play = self.scene.pop(0)
            return play

        return False

    def play_scene_message(self):
        """ play the message of the scene """
        print("displaying message: " + self.play["content"])
        self.drawer.add_message(self.play["content"])
        return True

    def play_spawn(self):
        """ play the spawn enemy of the scene """
        content = self.play["content"][0]
        """ get the enemy type """
        if content['type'] == "enemy":
            self.spawn_ship(content)
        return True

    def pause_time_start(self):
        """ pause the time """
        if self.pause_time is None:
            self.pause_time = time.time() * 1000

    def pause_time_stop(self):
        """ stop the pause time """
        if self.pause_time is not None:
            # Calculate the time spent paused and add it to paused_time
            self.paused_time += time.time() * 1000 - self.pause_time
            # Add the paused time to the messages
            self.drawer.adjust_messaged_for_paused_time(self.paused_time)
            # Add the paused time to the current time
            self.time += self.paused_time
            self.pause_time = None

    def spawn_ship(self, content):
        """ spawn a ship """
        if content["ship"] == "gravion":
            alien = Gravion(self.setting, self.bullets)
            self.aliens.add(alien)
            self.setting.my_game.music.warp_out()

    def play_scene_end(self):
        if not self.aliens:
            self.drawer.add_message("Level complete")
            self.end = False
        return True
