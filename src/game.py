import pygame
from pygame.sprite import Group
from src.setting import Setting
from src.sf_ship import SFship
from src.event import Event
from src.alien import Alien
from src.music import Music

class Game():
    # class game, game container

    def __init__(self):
        # run an instance of the game
        pygame.init()
    
        self.setting = Setting(pygame)
        self.setting.init_screen()

    
    def run(self):
        (ship, event, bullets, clock, aliens, music) = self.init_ojbects()       

        # Start the main loop for the game.
        while True:
            clock.tick(165)  # Limit the frame rate to 165 FPS (my monitor refresh rate)
            # Watch for keyboard and mouse events.
            event.check_events(ship, bullets)

            # Redraw the screen during each pass through the loop.
            self.update_screen(ship, bullets, aliens)

            # update ships
            ship.update()
            aliens.update() # TODO: free out of screen ships / generate more ships

            # update bullets
            self.update_bullets(bullets,aliens)

            # draw game score, and lives..
            self.setting.draw_game_info()

            # calculate FPS
            self.calculate_fps(clock)
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()


    def init_ojbects(self):
        # Make a ship.
        ship = SFship(self.setting)

        #music class init
        music = Music(self.setting)
        event = Event(pygame, self.setting, music)

        # Make a group to store bullets in.
        bullets = Group()

        # start the clock for the game
        clock = pygame.time.Clock()

        # create an alien
        aliens = Group()
        alien = Alien(self.setting, bullets)
        aliens.add(alien)

        return (ship, event, bullets, clock, aliens, music)
    

    def update_screen(self, ship, bullets, aliens):
        # update game screen
        self.setting.fill()
        ship.draw()
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        
        for alien in aliens.sprites():
            alien.draw()


    def update_bullets(self, bullets, aliens):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.setting.getScreenY():
                bullets.remove(bullet)
        
        # get all collisions
        collisions = pygame.sprite.groupcollide(bullets, aliens, False, False)
        # check if the collision is friendly or not
        for bullet, collided_aliens in collisions.items():
            # Call the 'is_friendly' method on the Bullet object
            if (bullet.is_friendly()):
                self.setting.game_score += 100
                aliens.remove(collided_aliens)
                aliens.add(Alien(self.setting, bullets))
                        


    def calculate_fps(self, clock):
        # Calculate FPS
        fps = clock.get_fps()
        fps_text = pygame.font.Font(None, 25).render(f"{fps:.0f}", True, [250,0,0])

        # Draw FPS text on the screen
        self.setting.screen.blit(fps_text, (self.setting.getScreenX() - 40, 10))