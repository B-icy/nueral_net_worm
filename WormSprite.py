import numpy as np
import pyglet
import random
import math
import resources

from CONSTANTS import *

class WormSprite():
    
    ROTATION_SPEED = 3
    MOVE_SPEED = 100
    
    def __init__(self, x, y, batch=None):
        self.x_min = LEFT
        self.x_max = RIGHT
        self.y_min = TOP
        self.y_max = BOTTOM

        self.sprite =  pyglet.sprite.Sprite(resources.wormie, x=0, y=0, batch=batch)
        self.sprite.rotation = random.randint(0, 360)
        self.rotation_in_radians = np.deg2rad(self.sprite.rotation)
        self.direction_vec = np.array( [np.cos(self.rotation_in_radians), np.sin(self.rotation_in_radians)] )
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2

        self.sprite.x = x
        self.sprite.y = y

        self.food_eaten = 0

        self.food_label = pyglet.text.Label(str(self.food_eaten),
                                            font_name='Calibri',
                                            font_size=15,
                                            x=self.sprite.x+30, y=self.sprite.y-30,
                                            anchor_x='center', anchor_y='center',
                                            color=(0,0,255,255),
                                            batch=batch)
        
    def update(self, dt, move, food=[]):
        # When traning model, comment out line below and manually call move each frame.
        # Moving randomly for demo purposes
        self.move( move , dt )
        self.near_food(food)

    def update_text(self,num_food_eaten):
        self.food_label.text = str(num_food_eaten)
        self.food_label.x, self.food_label.y = (self.sprite.x+30, self.sprite.y-30)

        

    # Movement is a float between -1 -> 1 adjusting the angle of the worm. -1 steers left, 1 steers right. I think...
    def move(self, direction, dt):
        self.sprite.rotation += direction * self.ROTATION_SPEED
        self.rotation_in_radians = np.deg2rad( -1 * self.sprite.rotation)
        direction_vec =  np.array( [np.cos(self.rotation_in_radians), np.sin(self.rotation_in_radians)] )
        
        self.sprite.x += direction_vec[0] * dt * self.MOVE_SPEED
        self.sprite.y += direction_vec[1] * dt * self.MOVE_SPEED

        if self.sprite.x < self.x_min + self.sprite.image.width / 2:
           self. sprite.x = self.x_min + self.sprite.image.width / 2
        elif self.sprite.x > self.x_max - self.sprite.image.width / 2:
            self.sprite.x = self.x_max - self.sprite.image.width / 2

        if self.sprite.y < self.y_min + self.sprite.image.width / 2:
            self.sprite.y = self.y_min + self.sprite.image.width / 2
        elif self.sprite.y > self.y_max - self.sprite.image.width / 2:
            self.sprite.y = self.y_max - self.sprite.image.width / 2

    def draw(self):
        self.sprite.draw()
        self.food_label.draw()

    def delete(self):
        self.sprite.delete()
        self.food_label.delete()

    def near_food(self, food):
        #distance_to_food = 100000
        quad_distance_to_food = np.array([MAX_SENSOR_DISTANCE for i in range(4)])
        quadrant = 0
        distance_to_food_tmp = 0 # fk creative names im tired
        food_eaten=False

         # fk efficiency
        for i in food:
            if(i.x!=DEFAULT_FOOD_VAL):
                distance_to_food_tmp = np.linalg.norm( np.array([self.sprite.x, self.sprite.y]) - np.array([i.x, i.y]) )
                # gl with this one lmao
                quadrant = (0 if i.x - self.sprite.x >= 0 else 1) + (0 if i.y - self.sprite.y >= 0 else 2)

                #eating food
                if distance_to_food_tmp < 50:
                    is_near_food = True
                    food_eaten=True
                    i.x, i.y = (DEFAULT_FOOD_VAL, DEFAULT_FOOD_VAL)

                # checking if it is closest food
                if  distance_to_food_tmp < quad_distance_to_food[quadrant]:
                    quad_distance_to_food[quadrant] = distance_to_food_tmp
            
        return quad_distance_to_food, food_eaten