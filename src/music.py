
# let's do the handling of our sounds here
class Music():

    def __init__(self, setting):
        self.setting = setting


    def shot_lazer(self):
        lazer = "resources/sounds/laser_shot_sound_lazer.wav"
        self.setting.game.mixer.music.load(lazer)

        # Play the music
        self.setting.game.mixer.music.play()