# let's do the handling of our sounds here
class Music:

    def __init__(self, setting):
        self.setting = setting
        self.setting.game.mixer.init()
        background_music = self.setting.game.mixer.Sound('resources/sounds/moonlightsonataspace.ogg')
        background_music.set_volume(0.5)
        # Start playing the background music on loop
        background_music.play(-1)

        self.lazer = self.setting.game.mixer.Sound("resources/sounds/laser_shot_sound_lazer.wav")
        self.lazer.set_volume(0.20)

        self.explosion = self.setting.game.mixer.Sound("resources/sounds/explosion.wav")
        self.explosion.set_volume(0.25)

        self.warp = self.setting.game.mixer.Sound("resources/sounds/drop-out-warp.wav")
        self.warp.set_volume(1)

    def shot_lazer(self):
        # Play the music
        self.lazer.play()

    def destroy_ship(self):
        self.explosion.play()

    def warp_out(self):
        self.warp.play()
