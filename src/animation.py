import time
from src.effect.explosion import Explosion


class Animation():
    """ class to handle all animations of our game """

    def __init__(self, setting) -> None:
        self.setting = setting
        self.explosions = []
        self.images = {}

    def add_explosion(self, x, y):
        # load the image if it's not loaded
        if 'explosion' not in self.images:
            self.images['explosion'] = self.setting.game.image.load("resources/images/explosion/animation.bmp")
        explosion = Explosion(self.setting, x, y, self.images['explosion'])
        self.explosions.append(explosion)

    def draw_all(self):
        self.draw_explosions()

    def draw_explosions(self):
        current_time = int(time.time() * 1000)
        explosions_to_remove = []

        for explosion in self.explosions:
            # check if expired
            if (current_time - explosion.get_created_at()) >= 2000:
                explosions_to_remove.append(explosion)
            else:
                explosion.update()
                explosion.draw()

        # Remove expired explosions
        for explosion in explosions_to_remove:
            self.explosions.remove(explosion)
