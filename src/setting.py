from src.parse_config import parse_config
import random

class Setting():
    """setting class to store all settings and update them"""

    def __init__(self, game):
        """parse config file, and put default values for missing infos"""
        """ return screen for drawing, and background color"""
        config = parse_config();
        game_window_config = {}
        if config is not None and "game_window" in config:
            game_window_config = config.get('game_window', {})
    
        game_bullet_config = {}
        if config is not None and "bullet" in config:
            game_bullet_config = config.get('bullet', {})
        
        # screen config
        self.screen_dimensions  = game_window_config.get('screen', [1200, 800])
        self.background_color   = game_window_config.get('background', [40, 40, 40])
        self.window_description = game_window_config.get('description', "Alien Invasion")

        # bullet config
        self.bullet_speed_factor = game_bullet_config.get('speed_factor', 1)
        self.bullet_width        = game_bullet_config.get('width', 3)
        self.bullet_height       = game_bullet_config.get('height', 15)
        self.bullet_color        = game_bullet_config.get('color', [60, 60, 60])
        self.bullet_allowed      = game_bullet_config.get('allowed_number', 7)

        self.screen             = None
        self.game               = game

        ## load stars images
        star  = game.image.load('resources/images/star_01.bmp')
        score = game.image.load('resources/images/score_icon.bmp')

        self.score = game.transform.scale(score, (25, 25))
        self.star  = game.transform.scale(star, (25, 25))
        self.rect  = self.star.get_rect()
        self.stars = []
        self.game_score = 0


    def getScreenX(self):
        _, _, x, _ = self.screen_rect
        return x
    

    def getScreenY(self):
        _, _, _, y = self.screen_rect
        return y


    def init_screen(self):
        """initiate new game window with current config"""
        self.screen = self.game.display.set_mode(self.screen_dimensions)
        self.game.display.set_caption(self.window_description)
        self.screen_rect = self.screen.get_rect()


    def fill(self):
        """ fill the window with our background color """
        self.screen.fill(self.background_color)

        # add stars to the sky
        self.draw_stars()


    def draw_stars(self):
        if (self.stars):
            # we already have created the list let's move the stars and display them
            for i, (x, y) in enumerate(self.stars):
                self.stars[i] = (x, y + 1) # TODO: change to be relative to the speed of the ship
                if (y > self.getScreenY()):
                    self.stars[i] = (random.randint(0, self.getScreenX()), -20)
                self.screen.blit(self.star, (x, y))
        else:
            # Create a list to store star positions for first run
            stars = []

            # Generate random star positions
            for _ in range(100):  # You can adjust the number of stars as desired
                x = random.randint(0, self.getScreenX())  # Random x-coordinate within the screen width
                y = random.randint(0, self.getScreenY())   # Random y-coordinate within the screen height
                stars.append((x, y))
                self.screen.blit(self.star, [x, y])
            self.stars = stars

    
    def draw_game_info(self):
        # draw score
        self.screen.blit(self.score, (10, 10))
        score = self.game.font.Font(None, 25).render(f"{self.game_score:.0f}", True, [250,250,250])

        # Draw FPS text on the screen
        self.screen.blit(score, (40, 18))