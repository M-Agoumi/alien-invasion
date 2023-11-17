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
        
        game_specs_config = {}
        if config is not None and "game_specs" in config:
            game_specs_config = config.get('game_specs', {})

        self.background_color   = game_window_config.get('background', [40, 40, 40])
        self.window_description = game_window_config.get('description', "Alien Invasion")

        # bullet config
        self.bullet_speed_factor = game_bullet_config.get('speed_factor', 1)
        self.bullet_width        = game_bullet_config.get('width', 3)
        self.bullet_height       = game_bullet_config.get('height', 15)
        self.bullet_color        = game_bullet_config.get('color', [60, 60, 60])
        self.bullet_allowed      = game_bullet_config.get('allowed_number', 7)

        self.sf_ship_lives      = game_specs_config.get('lives', 3)

        self.screen             = None
        self.game               = game

        ## load stars images
        star  = game.image.load('resources/images/star_01.bmp')
        score = game.image.load('resources/images/score_icon.bmp')
        hp    = game.image.load('resources/images/heart.bmp')
        ship  = game.image.load('resources/images/spaceship_icon.bmp')

        self.score     = game.transform.scale(score, (25, 25))
        self.star      = game.transform.scale(star, (25, 25))
        self.hp_icon   = game.transform.scale(hp, (25, 25))
        self.ship_icon = game.transform.scale(ship, (25, 40))
        self.rect      = self.star.get_rect()
        self.stars     = []
        self.game_score = 0


    def getScreenX(self):
        _, _, x, _ = self.screen_rect
        return x
    

    def getScreenY(self):
        _, _, _, y = self.screen_rect
        return y


    def init_screen(self, width, height):
        """initiate new game window in full screen"""
        self.screen = self.game.display.set_mode((width, height), self.game.FULLSCREEN)
        self.game.display.set_caption(self.window_description)
        self.screen_rect = self.screen.get_rect()

        # Take image as input 
        img = self.game.image.load('icon.jpeg') 
        
        # Set image as icon 
        self.game.display.set_icon(img)


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

    
    def draw_game_info(self, clock, ship):
        # draw score
        self.screen.blit(self.score, (10, 10))
        score = self.game.font.Font(None, 25).render(f"{self.game_score:.0f}", True, [250,250,250])
        # draw hp
        self.screen.blit(self.hp_icon, (10, 50))
        hp = self.game.font.Font(None, 25).render(f"{ship.get_hp():.0f}", True, [250,250,250])
        # draw ship lives
        self.screen.blit(self.ship_icon, (10, 80))
        lives = self.game.font.Font(None, 25).render(f"{self.sf_ship_lives:.0f}", True, [250,250,250])

        # Draw FPS text on the screen
        self.screen.blit(score, (40, 18))
        self.screen.blit(hp, (40, 50))
        self.screen.blit(lives, (43, 90))

        # calculate FPS
        self.calculate_fps(clock)




    def calculate_fps(self, clock):
        # Calculate FPS
        fps = clock.get_fps()
        fps_text = self.game.font.Font(None, 25).render(f"{fps:.0f}", True, [250,0,0])

        # Draw FPS text on the screen
        self.screen.blit(fps_text, (self.getScreenX() - 40, 10))