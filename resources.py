import pyglet

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

wormie = pyglet.resource.image("wormie.png")
wormie_ded = pyglet.resource.image("wormie_ded.png")
food = pyglet.resource.image("food.png")
