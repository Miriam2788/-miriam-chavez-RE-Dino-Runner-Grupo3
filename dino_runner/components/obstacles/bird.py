import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import (BIRD)




class Birds(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image,self.type)
        if self.image == BIRD:
            self.rect.y = 225
        
