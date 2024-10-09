'''
This script has class Wheel with its methods
'''

from pygame import image, transform

class Wheel:
    """
    Wheel class
    """
    def __init__(self) -> None:
        self.image = transform.scale(image.load("sprites/steering_wheel.png").convert_alpha(),
                                     (410.6, 302.4))

    def functioning(self, screen, x):
        '''
        This method is responsible for drawing a wheel and turning it
        '''
        angle = x * -90
        image_copy = transform.rotate(self.image, angle)
        screen.blit(image_copy, (screen.get_rect().center[0] - int(image_copy.get_width()/2),
                                 screen.get_rect().center[1]+170 - int(image_copy.get_height()/2)) )
