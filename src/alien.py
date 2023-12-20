from pygame.sprite import Sprite
from src.warship import Warship
from src.bullet import Bullet
import random
import time


# class for the aliens of our game
class Alien(Sprite, Warship):

    def __init__(self, setting, bullets):
        """Initialize the alien and set its starting position."""
        # super(Alien, self).__init__(setting, 'resources/images/alien_1.bmp', 60, 70, 1)
        # super(Sprite).__init__()
        # self.setting = setting
        # self.place_ship()

        """Initialize the alien and set its starting position."""
        super().__init__()
        Warship.__init__(self, setting, 'resources/images/alien_2.bmp', 60, 70, 10)
        self.setting = setting
        self.place_ship()

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.last_firing_time = (time.time() - 3)

        if random.getrandbits(1):
            self.moving_right = True
        else:
            self.moving_left = True
        # moving with speed factor make spaceship move fast in Y
        # and since position is an int we introduce this variable that's
        # going to have float value
        self.move_down = 0

        self.bullets = bullets

        self.hp = 100

    def place_ship(self):
        # Start each new ship at a random point of the top of the screen.
        self.rect.centerx = random.randrange(0, self.setting.get_screen_x())
        self.rect.top = -100

    def fire(self):
        # fire a bullet if the alien ship isn't reloading
        # TODO: add more firing patterns
        # TODO: debug missing bullets
        current_time = time.time()
        if (current_time - self.last_firing_time) > 3:
            new_bullet = Bullet(self.setting, self.setting.screen, self, 0)
            self.bullets.add(new_bullet)
            self.last_firing_time = current_time

    def update(self):
        self.fire()
        """TODO: Update the ship's position based on the movement flag."""
        # randomly move ship
        if self.moving_right and self.rect.right >= self.screen_rect.right:
            self.moving_right = False
            self.moving_left = True

        if self.moving_left and self.rect.left <= 0:
            self.moving_right = True
            self.moving_left = False

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.speed_factor

        # move downside toward the player
        if self.rect.top > 20:
            self.speed_factor = 1
        self.move_down += 10 * self.speed_factor
        if self.move_down >= 100:
            self.rect.top += 1
            self.move_down = 0

    def update_hp(self, hp):
        self.ship_hp -= hp
        return self
