import pygame
from pygame.sprite import Sprite

#class for ships bullet, we need to track them
class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, setting, screen, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen
        
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, setting.bullet_width,
        setting.bullet_height)
        self.rect.centerx = ship.rect.centerx - 1
        self.rect.top = (ship.rect.top - 12)
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

        self.color = setting.bullet_color
        self.speed_factor = setting.bullet_speed_factor

    
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)