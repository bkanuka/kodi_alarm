import sys
import time

class Amp:
    def __init__(self, harmony):
        self.harmony=harmony

    def volume_up(self):
        self.harmony.volume_up()

    def volume_down(self):
        self.harmony.volume_up()
