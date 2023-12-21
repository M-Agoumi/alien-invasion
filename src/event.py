import sys
from src.bullet import Bullet


def get_bullets_count(bullets):
    total_bullets = 0
    for bullet in bullets:
        if bullet.is_friendly():
            total_bullets += 1
    return total_bullets


class Event:
    # Handle game events (keyboard and mouse clicks)

    def __init__(self, game, setting, music):
        self.game = game
        self.setting = setting
        self.music = music

    def check_events(self, ship, bullets):
        for event in self.game.event.get():
            if event.type == self.game.QUIT:
                sys.exit()

            elif event.type == self.game.KEYDOWN:
                self.check_keydown_events(event, ship, bullets)

            elif event.type == self.game.KEYUP:
                self.check_keyup_events(event, ship)

    def check_keydown_events(self, event, ship, bullets):
        if event.key == self.game.K_d or event.key == self.game.K_RIGHT:
            # Move the ship to the right.
            ship.moving_right = True
        elif event.key == self.game.K_a or event.key == self.game.K_LEFT:
            # Move the ship to the left.
            ship.moving_left = True
        elif event.key == self.game.K_SPACE:
            self.fire_bullet(bullets, ship)
        elif event.key == self.game.K_p:
            self.setting.pause = not self.setting.pause
        elif event.key == self.game.K_q:
            sys.exit()

    def check_keyup_events(self, event, ship):
        if event.key == self.game.K_d or event.key == self.game.K_RIGHT:
            ship.moving_right = False
        if event.key == self.game.K_a or event.key == self.game.K_LEFT:
            ship.moving_left = False

    def fire_bullet(self, bullets, ship):
        # Create a new bullet and add it to the bullets group.
        total_bullets = get_bullets_count(bullets)
        if total_bullets < self.setting.bullet_allowed:
            new_bullet = Bullet(self.setting, self.setting.screen, ship)
            bullets.add(new_bullet)
            self.music.shot_lazer()
