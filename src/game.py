import pygame
from pygame.sprite import Group
from src.setting import Setting
from src.ship import Ship
from src.event import Event

class Game():
    # class game, game container

    def __init__(self):
        # run an instance of the game
        pygame.init()
    
        self.setting = Setting(pygame)
        self.setting.init_screen()

    
    def run(self):
        (ship, event, bullets, clock) = self.init_ojbects()       

        # Start the main loop for the game.
        while True:
            clock.tick(80)  # Limit the frame rate to 60 frames per second
            # Watch for keyboard and mouse events.
            event.check_events(ship, bullets)

            # Redraw the screen during each pass through the loop.
            self.update_screen(ship, bullets)

            # update ship
            ship.update()

            # update bullets
            self.update_bullets(bullets)

            # draw game score, and lives..
            self.setting.draw_game_info()

            # calculate FPS
            self.calculate_fps(clock)
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()


    def init_ojbects(self):
        # Make a ship.
        ship = Ship(self.setting.screen, self.setting.game)
        event = Event(pygame, self.setting)

        # Make a group to store bullets in.
        bullets = Group()

        # start the clock for the game
        clock = pygame.time.Clock()

        return (ship, event, bullets, clock)
    

    def update_screen(self, ship, bullets):
        # update game screen
        self.setting.fill()
        ship.blitme()
        for bullet in bullets.sprites():
            bullet.draw_bullet()


    def update_bullets(self, bullets):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

    def calculate_fps(self, clock):
        # Calculate FPS
        fps = clock.get_fps()
        fps_text = pygame.font.Font(None, 25).render(f"{fps:.0f}", True, [250,0,0])

        # Draw FPS text on the screen
        self.setting.screen.blit(fps_text, (self.setting.getScreenX() - 40, 10))
        