from __future__ import division

from pyglet.window import key
import pyglet
import resources
import numpy as np

import random
import math

from Worm import Worm

from CONSTANTS import *


class Dead_Worm_Container():
    DESPAWN_SECONDS = 3

    def __init__(self):
        self.worms = []
        self.dead_worm_batch = pyglet.graphics.Batch()

    def update(self, dt):
        for i in reversed(self.worms):
            i[1] -= dt
            if i[1]  < 0:
                self.worms.remove(i)

    def draw(self):
        self.dead_worm_batch.draw()

    def add_worm(self, x, y, rotation):
        sprite = pyglet.sprite.Sprite(resources.wormie_ded, x=x, y=y,batch=self.dead_worm_batch)
        sprite.rotation = rotation
        sprite.image.anchor_x = sprite.image.width / 2
        sprite.image.anchor_y = sprite.image.height / 2
        self.worms.append([sprite, self.DESPAWN_SECONDS])

class Worm_Container():
    DEATH_TIMER = 10

    def __init__(self, num_worms):
        self.worm_batch = pyglet.graphics.Batch()
        self.worms = []
        self.dead_worms = Dead_Worm_Container()
        for i in range(num_worms):
            self.add_worm()

        self.timer = 0

    def update(self, dt, food):
        for w in self.worms:
            food_distances, ate = w.sprite.near_food(food)
            next_move = w.get_move(food_distances)
            #print(next_move)
            if ate: w.food_eaten+=1
            w.sprite.move( next_move , dt )
            w.sprite.update_text(w.food_eaten)
        self.timer += dt
        if self.timer >= GENERATION_LENGTH:
            self.timer=0
            self.worms.sort()
            self.kill_starved_worms()
            self.make_babies()
            self.fill_pop()
        self.dead_worms.update(dt)

    def add_worm(self):
        x = random.randint(LEFT+100,RIGHT-100)
        y = random.randint(TOP+100,BOTTOM-100)
        new_worm = Worm(self.worm_batch,x,y,None)
        self.worms.append(new_worm)

    #input is sorted
    def kill_starved_worms(self):
        for w,i in zip(self.worms,range(len(self.worms))):
            if(w.food_eaten==0):
                self.dead_worms.add_worm(w.sprite.sprite.x, w.sprite.sprite.y,w.sprite.sprite.rotation)
            else:
                #delete all worms leading up to this
                for k in range(i):
                    self.delete(0)
                return
        #if no worms got food, kill them all
        self.worms=[]

    def make_babies(self):
        #basically for every food over 1 spawn a child
        babies=[]
        for w in self.worms:
            assert w.food_eaten>0
            print(f"worm has eaten {w.food_eaten} food")
            for i in range(1,w.food_eaten):
                #have baby have similar pos to parent
                x = BABY_SPAWN_OFFSET*np.random.randn()+w.sprite.sprite.x
                y = BABY_SPAWN_OFFSET*np.random.randn()+w.sprite.sprite.y
                new_worm = Worm(sprite_batch=self.worm_batch,x=x,y=y,parent=w)
                #have baby have similar pos to parent
                babies.append(new_worm)
            w.food_eaten=0
        self.worms+=babies

    def fill_pop(self):
        while(len(self.worms)<MIN_WORMS):
            self.add_worm()
    

    def delete(self, index):
        self.worms.pop(index).sprite.delete()
    
    def draw(self):
        self.worm_batch.draw()
        self.dead_worms.draw()



class Food_Container():
    
    SPAWN_RATE = 10
    MAX_PELLETS = 50
    
    food_batch = pyglet.graphics.Batch()
    food_pellets = np.empty([MAX_PELLETS],dtype=pyglet.sprite.Sprite)

    def __init__(self):
        self.x_min = LEFT
        self.x_max = RIGHT
        self.y_min = TOP
        self.y_max = BOTTOM

        for i in range(self.MAX_PELLETS):
            self.food_pellets[i] = pyglet.sprite.Sprite(resources.food, x=DEFAULT_FOOD_VAL, y=DEFAULT_FOOD_VAL,batch=self.food_batch)
            self.food_pellets[i].image.anchor_x = self.food_pellets[i].image.width / 2
            self.food_pellets[i].image.anchor_y = self.food_pellets[i].image.height / 2
        self.add_food(5)

    def update(self, dt):
        if 1 > random.randint(0,1000 * (1 / self.SPAWN_RATE)):
            self.add_food(1)

    def draw(self):
        self.food_batch.draw()
    
    def add_food(self, amount):
        for i in self.food_pellets:
            if amount <= 0:
                break
            if i.x < 0 and i.y < 0:
                    amount -= 1
                    i.x = random.randint(self.x_min + i.image.width, self.x_max - i.image.width)
                    i.y = random.randint(self.y_min + i.image.width, self.y_max - i.image.width)
        return
                    

    

# Initialize stuff
window = pyglet.window.Window(width=RIGHT-LEFT, height=BOTTOM-TOP, caption="Worm Lyfe")
window.set_mouse_visible(False)



@window.event
def on_draw():
    window.clear()

    fud.draw()
    #wormie.draw()
    worm_container.draw()

    #near_food_label.draw()
    #food_eaten_label.draw()

def update(dt):
    #wormie.update(dt)
    worm_container.update(dt, fud.food_pellets)
    fud.update(dt)

    #near_food_label.text = "Closest food: " + str(wormie.near_food(fud.food_pellets))
    #food_eaten_label.text = 'Food eaten: ' + str(wormie.food_eaten)


if __name__ == '__main__':

    #Background color
    pyglet.gl.glClearColor(1., .9, .3, .1)

    #main worm, didnt want to get rid of him
    #wormie = Worm(window.width/2, window.height/2)
    worm_container = Worm_Container(MIN_WORMS)
    fud = Food_Container()

    

    # near_food_label = pyglet.text.Label('Closest food: ' + str(wormie.near_food(fud.food_pellets)),
    #                       font_name='Calibri',
    #                       font_size=20,
    #                       x=3 * window.width//4, y=window.height - 20,
    #                       anchor_x='center', anchor_y='center', color=(0,0,255,255))

    # food_eaten_label = pyglet.text.Label('Food eaten: ' + str(wormie.food_eaten),
    #                       font_name='Calibri',
    #                       font_size=36,
    #                       x=300, y=window.height - 20,
    #                       anchor_x='center', anchor_y='center', color=(0,0,255,255))
    
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()
