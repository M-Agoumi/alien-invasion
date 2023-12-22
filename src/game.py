import pygame, os
import time
from sys import exit
from pygame.sprite import Group

from src.drawer import Drawer
from src.level.level import Level
from src.parser import Parser
from src.setting import Setting
from src.sf_ship import SFship
from src.event import Event
from src.music import Music
from src.animation import Animation


class Game:
    # class game, game container

    def __init__(self):
        self.level = None
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        os.environ['PYGAME_DETECT_AVX2'] = '1'
        # run an instance of the game
        pygame.init()

        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        parser = Parser()
        self.setting = Setting(pygame, parser, self)
        self.setting.init_screen(self.screen_width, self.screen_height)
        self.animation = Animation(self.setting)
        self.game_was_paused = False
        self.music = None

    def run(self):
        (ship, event, bullets, clock, aliens, music, level, drawer) = self.init_objects()

        # Start the main loop for the game.
        while True:
            clock.tick(165)  # Limit the frame rate to 165 FPS (my monitor refresh rate)
            # Make the most recently drawn screen visible.
            pygame.display.flip()

            # Watch for keyboard and mouse events.
            event.check_events(ship, bullets)

            if self.setting.pause:
                self.setting.pause_game(drawer)
                self.game_was_paused = True
                continue
            elif self.game_was_paused:
                self.game_was_paused = False
                level.pause_time_stop()

            # Redraw the screen during each pass through the loop.
            self.update_screen(ship, bullets, aliens)

            # update ships
            ship.update()
            level.play_level()
            aliens.update()  # TODO: free out of screen ships / generate more ships
            self.animation.draw_all()

            # update bullets
            self.update_bullets(bullets, aliens, ship, music)

            # draw game score, and lives...
            drawer.draw_game_info(clock, ship)

    def init_objects(self):
        # Make a ship.
        ship = SFship(self.setting)

        # music class init
        self.music = Music(self.setting)

        event = Event(pygame, self.setting, self.music)

        # Make a group to store bullets in.
        bullets = Group()

        # start the clock for the game
        clock = pygame.time.Clock()

        # create an alien
        aliens = Group()

        # create drawer
        drawer = Drawer(pygame, self.setting)
        # create a level object
        level = Level(self.setting, drawer, bullets, aliens)
        self.level = level

        return ship, event, bullets, clock, aliens, self.music, level, drawer

    def update_screen(self, ship, bullets, aliens):
        # update game screen
        self.setting.fill()
        ship.draw()
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        for alien in aliens.sprites():
            alien.draw()

    def update_bullets(self, bullets, aliens, ship, music):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.setting.get_screen_y():
                bullets.remove(bullet)

        # get all collisions
        collisions = pygame.sprite.groupcollide(bullets, aliens, False, False)
        # check if the collision is friendly or not
        for bullet, collided_aliens in collisions.items():
            # Call the 'is_friendly' method on the Bullet object
            if bullet.is_friendly():
                self.setting.game_score += 100
                music.destroy_ship()
                for alien in collided_aliens:
                    self.animation.add_explosion(alien.rect.left, alien.rect.top)
                aliens.remove(collided_aliens)
                bullets.remove(bullet)

        # check for collision with our spaceship
        for bullet in bullets:
            if bullet.is_friendly() == 0:
                if ((ship.rect.left <= bullet.rect.centerx <= ship.rect.right) and
                        bullet.rect.bottom >= ship.rect.top):
                    bullets.remove(bullet)
                    ship.update_hp(50)
                    if ship.get_hp() <= 0:
                        self.setting.sf_ship_lives -= 1
                        ship.post_die()
                    if self.setting.sf_ship_lives <= 0:
                        self.end_game()

    def debug_grid(self):
        # Draw horizontal grid lines
        for y in range(0, 800, 20):
            self.setting.game.draw.line(self.setting.screen, [0, 0, 255], (0, y), (1200, y), 1)
            text = self.setting.game.font.Font(None, 20).render(f"{y:.0f}", True, [250, 250, 250])
            self.setting.screen.blit(text, (5, y - 10))

        tmp = False
        # Draw vertical grid lines
        for x in range(0, 1200, 20):
            self.setting.game.draw.line(self.setting.screen, [0, 255, 0], (x, 0), (x, 800), 1)
            if tmp:
                text = self.setting.game.font.Font(None, 20).render(f"{x:.0f}", True, [250, 250, 250])
                self.setting.screen.blit(text, (x + 5, 5))
                tmp = False
            else:
                tmp = True

    def end_game(self):
        print("you died, and you have no life left, game over")
        self.setting.game.quit()
        exit()
