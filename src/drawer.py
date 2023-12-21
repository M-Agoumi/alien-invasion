import time

import pygame


class Drawer:
    def __init__(self, game, setting):
        """ Initialize drawer """
        self.game = game
        self.setting = setting
        self.screen = setting.screen
        self.messages = []

    def draw_game_info(self, clock, ship):
        # draw score
        self.screen.blit(self.setting.score, (10, 10))
        score = self.game.font.Font(None, 25).render(f"{self.setting.game_score:.0f}", True, [250, 250, 250])
        # draw hp
        self.screen.blit(self.setting.hp_icon, (10, 50))
        hp = self.game.font.Font(None, 25).render(f"{ship.get_hp():.0f}", True, [250, 250, 250])
        # draw ship lives
        self.screen.blit(self.setting.ship_icon, (10, 80))
        lives = self.game.font.Font(None, 25).render(f"{self.setting.sf_ship_lives:.0f}", True, [250, 250, 250])

        # Draw FPS text on the screen
        self.screen.blit(score, (40, 18))
        self.screen.blit(hp, (40, 50))
        self.screen.blit(lives, (43, 90))

        # Draw messages
        self.draw_message()

        # calculate FPS
        self.calculate_fps(clock)

    def calculate_fps(self, clock):
        # Calculate FPS
        fps = clock.get_fps()
        fps_text = self.game.font.Font(None, 25).render(f"{fps:.0f}", True, [250, 0, 0])

        # Draw FPS text on the screen
        self.screen.blit(fps_text, (self.setting.get_screen_x() - 40, 10))

    def add_message(self, message):
        """ draw message on the screen """
        self.messages.append({"message": message, "timestamp": time.time() * 1000})

    def adjust_messaged_for_paused_time(self, paused_time):
        for message in self.messages:
            message["timestamp"] += paused_time

    def draw_message(self):
        for message in self.messages:
            if (time.time() * 1000) - message["timestamp"] > 3000:
                self.messages.remove(message)
            self.draw_text_with_outline(message["message"], 125, (800, 500), (250, 250, 250),
                                        (0, 0, 255))

    def draw_text_with_outline(self, text, font_size, position, text_color, outline_color, background_color=None,
                               border_radius=0):
        # Render the original text
        text_surface = self.game.font.Font(None, font_size).render(text, True, text_color)

        # Calculate the size of the background based on the text size
        background_rect = text_surface.get_rect()
        background_rect.inflate_ip(10, 10)  # Adjust the padding as needed

        # Draw the background if a background color is provided
        if background_color:
            background_rect.topleft = position  # Set the background position to the specified position
            pygame.draw.rect(self.screen, background_color, background_rect, border_radius=border_radius)

        # Calculate the position to center the text within the background
        text_position = (position[0] + (background_rect.width - text_surface.get_width()) // 2,
                         position[1] + (background_rect.height - text_surface.get_height()) // 2)

        # Render the text with an outline
        text_outline = self.game.font.Font(None, font_size + 2).render(text, True, outline_color)

        # Blit the outline first, then the original text on top
        self.screen.blit(text_outline, (text_position[0] - 1, text_position[1] - 1))
        self.screen.blit(text_outline, (text_position[0] + 1, text_position[1] - 1))
        self.screen.blit(text_outline, (text_position[0] - 1, text_position[1] + 1))
        self.screen.blit(text_outline, (text_position[0] + 1, text_position[1] + 1))
        self.screen.blit(text_surface, text_position)

    def draw_pause(self):
        self.draw_text_with_outline("PAUSE", 75, (875, 525), (250, 250, 250),
                                    (0, 0, 255), (50, 50, 50), 7)
