import time

class Explosion:
    ''' Class for the explosion animation for the alien ship destruction'''
    def __init__(self, setting, x, y, image):
        # Load the sprite sheet for the explosion animation
        self.setting = setting
        self.sheet = image
        self.frame_width = 250
        self.frame_height = 250
        self.scaled_frame_size = (75, 75)
        self.num_frames = 45  # Total number of frames
        self.frames_per_row = self.num_frames  # Assuming all frames in a single row
        self.frame_duration = 50  # 50 milliseconds per frame
        self.current_frame = 0
        self.x = x
        self.y = y
        self.created = time.time() * 1000  # Store creation time in milliseconds

    def get_created_at(self):
        return self.created

    def draw(self):
        frame_col = self.current_frame % self.frames_per_row
        frame_rect = self.setting.game.Rect(frame_col * self.frame_width, 0, self.frame_width, self.frame_height)
        frame_image = self.sheet.subsurface(frame_rect)
        scaled_frame = self.setting.game.transform.scale(frame_image, self.scaled_frame_size)
        self.setting.screen.blit(scaled_frame, (self.x, self.y))

    def update(self):
        elapsed_time = int(time.time() * 1000) - self.created
        # Calculate the current frame based on elapsed time and frame duration
        self.current_frame = min(self.num_frames - 1, elapsed_time // self.frame_duration)

    def is_finished(self):
        # Check if the animation has finished playing
        return self.current_frame == self.num_frames - 1
