"""
This file is drawing a window for simuation
"""

import pygame
from pygame import display, event, time, transform, image
from serial_decode import live_transmission
from wheel import Wheel

class Sim:
    '''
    Simulation at its finest
    '''
    def __init__(self) -> None:
        self.screen = display.set_mode((1280, 720))
        self.running = True
        self.clock = time.Clock()
        self.wheel = Wheel()
        self.background = transform.scale(image.load("sprites/cockpit.jpeg").convert(),
                                     (1280, 720))

    def run(self):
        """
        This method is responsible for running the simulation
        """
        x = 0 #імітація зміннох переданої від джойстика
        is_x = True
        while self.running:
            display.set_caption("Simulation")
            self.screen.fill("#FFFFFFFF")
            if is_x:
                res = live_transmission()
                print(res)
                if res > 0.35 and x <= 1:
                    x += 0.01
                elif res <= 0.35 and x >= -1:
                    x -= 0.01
                is_x = False
            else:
                is_x = True
            self.screen.blit(self.background, (0, 0))
            self.wheel.functioning(self.screen, x)
            self.clock.tick(60)
            for ev in event.get():
                if ev.type == pygame.QUIT:
                    self.running = False

            # ПОКи що поворот керма визначається натисканням/зажиманням стрілочок
            # keys=pygame.key.get_pressed()
            # if keys[pygame.K_RIGHT]:
            #     if x <= 1:
            #         x += 0.01
            # if keys[pygame.K_LEFT]:
            #     if x >= -1:
            #         x -= 0.01

            display.update()

if __name__ == "__main__":
    simulator = Sim()
    simulator.run()
