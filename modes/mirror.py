# modes/mirror.py

from game import Game


class MirrorMode:
    """Same rules as Timed Bloom — the twist is purely visual (the webcam
    feed is shown un-mirrored). Delegates all scoring/timer logic to a
    Game instance locked to level 1 (Timed Bloom) so the rules stay in
    one place."""

    def __init__(self):
        self.game = Game()
        self.game.set_level(1)

    def reset(self):
        self.game.set_level(1)

    def update(self, confirmed_gesture, flower):
        self.game.update(confirmed_gesture, flower)

    @property
    def game_over(self):
        return self.game.game_over

    @property
    def level_complete(self):
        return self.game.level_complete

    @property
    def score(self):
        return self.game.score

    @property
    def flowers_bloomed(self):
        return self.game.flowers_bloomed

    @property
    def time_left(self):
        return self.game.time_left

    @property
    def targets(self):
        return self.game.targets

    @property
    def collection(self):
        return self.game.collection

    @property
    def current_color_name(self):
        return self.game.current_color_name
