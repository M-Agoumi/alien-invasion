from abc import ABC, abstractmethod

class Warship(ABC):
    # Parent class for all warships

    def __init__(self, setting, ship_image, ship_x, ship_y, speed_factore):
        """Initialize the ship and set its starting position."""
        self.game = setting.game
        self.screen = setting.screen

        # Load the alien image and set its rect attribute.
        alien_image = setting.game.image.load(ship_image)
        self.image  = setting.game.transform.scale(alien_image, (ship_x, ship_y))
        self.rect   = self.image.get_rect()
        self.screen_rect = setting.screen.get_rect()

        self.moving_right = False
        self.moving_left  = False

        self.speed_factor = speed_factore
        self.ship_hp      = 100


    @abstractmethod
    def place_ship(self):
        pass


    def draw(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    
    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.speed_factor