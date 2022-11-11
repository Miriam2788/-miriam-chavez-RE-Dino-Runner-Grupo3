from dino_runner.utils.constants import (HAMMER, HAMMER_TYPE)
from dino_runner.components.power_ups.powerup import PowerUp

class HamerPowerUp(PowerUp):
    def __init__(self):
        self.image = HAMMER
        self.type = HAMMER_TYPE
        super(HamerPowerUp, self).__init__(self.image, self.type)