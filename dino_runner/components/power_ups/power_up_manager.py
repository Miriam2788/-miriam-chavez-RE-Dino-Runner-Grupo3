import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer_power_up import HamerPowerUp
from dino_runner.utils.constants import (HAMMER_POWER_UP)

class PowerUPManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.poins = 0
        self.option_numbers = list(range(1, 10))

    def reset_power_ups(self, points):
        self.power_ups = []
        self.points = points
        self.when_appears = random.randint(200, 300) + self.points

    def gennerate_power_ups(self, poins):
        self.poinst = poins
        if len(self.power_ups) == 0:
            if self.when_appears == self.poinst:
                print("generate powerup")
                self.when_appears = random.randint(self.when_appears + 200, self.when_appears + 250)
                random.shuffle(self.option_numbers)
                if self.option_numbers[0] <= 5:
                    self.power_ups.append(Shield())
                else:
                    self.power_ups.append(HamerPowerUp())
        return self.power_ups

    def update(self, points, game_speend, player):
        self.gennerate_power_ups(points)
        for power_up in self.power_ups:
            power_up.update(game_speend, self.power_ups)
            if player.dino_rect_colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                if isinstance(power_up, Shield):
                    player.shield = True
                    player.show_text = True
                    player.type = power_up.type
                    power_up.start_time = pygame.time.get_ticks()
                    time_random = random.randrange(5, 8)
                    player.shield_time_up = power_up.start_time + (time_random + 1000)
                    self.power_ups.remove(power_up)
                elif isinstance(power_up, HamerPowerUp):
                    player.hamer_enabled = HAMMER_POWER_UP
                    player.type = (power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)                    