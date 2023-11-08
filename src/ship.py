import time

class Ship():

    def __init__(self, screen, game):
        """Initialize the ship and set its starting position."""
        self.game = game
        self.screen = screen

        # Load the ship image and get its rect.
        self.image = game.image.load('resources/images/spaceship_2.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom  = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left  = False

        self.speed_factor = 2
        self.ship_hp      = 100

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.speed_factor

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)