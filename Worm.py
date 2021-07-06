

import numpy as np
from WormSprite import WormSprite
import random
import copy

from Network import Net
from CONSTANTS import *

class Worm():
    def __init__(self,sprite_batch,x,y,parent=None):
        self.sprite = WormSprite(x,y, batch=sprite_batch)
        self.food_eaten=0
        if(parent==None):
            self.brain=Net()
        else:
            self.brain=self.mutate_offspring_brain(parent.brain)

    def get_move(self,food_sensor):
        return self.brain.turn(food_sensor)

    def mutate_offspring_brain(self,parent_brain):
        new_brain = copy.deepcopy(parent_brain)
        new_brain.mutate()
        return new_brain

    def __lt__(self, other):
        return self.food_eaten < other.food_eaten

    def __str__(self):
        return f"<Worm:{self.food_eaten}>"
        

    # def get_move(self,food_sensor):
    #     d = np.argmin(food_sensor)
    #     if(d==0):
    #         return -0.5
    #     elif(d==1):
    #         return 0
    #     elif(d==2):
    #         return 0.5
    #     elif(d==3):
    #         return 1