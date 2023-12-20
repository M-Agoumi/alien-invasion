from src.warship import Warship


# Space Force Ship (ally | player's ship)
class SFship(Warship):

    def __init__(self, setting):
        super(SFship, self).__init__(setting, 'resources/images/spaceship_1.bmp', 50, 80, 2)
        self.place_ship()

    def place_ship(self):
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def update_hp(self, hp):
        self.ship_hp -= hp

    def post_die(self):
        self.ship_hp = 100
