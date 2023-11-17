import sys
from src.bullet import Bullet

class Event():
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
        elif event.key == self.game.K_q:
            sys.exit()
    

    def check_keyup_events(self, event, ship):
        if event.key == self.game.K_d or event.key == self.game.K_RIGHT:
            ship.moving_right = False
        if event.key == self.game.K_a or event.key == self.game.K_LEFT:
            ship.moving_left = False

    
    def fire_bullet(self, bullets, ship):
        # TODO: enemy bullets are counted in the limit fix that :)
        # TODO: play sound
        if len(bullets) < self.setting.bullet_allowed:
                new_bullet = Bullet(self.setting, self.setting.screen, ship)
                bullets.add(new_bullet)
                self.music.shot_lazer()