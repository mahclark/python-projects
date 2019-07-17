import random, math
import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font
from pyglet.window import key 

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()
                          
def collision(obj1, obj2):
    cond1 = (obj1.x <= obj2.x <= obj1.x + obj1.height) and (obj1.y <= obj2.y <= obj1.y + obj1.width)
    cond2 = (obj1.x <= obj2.x + obj2.height <= obj1.x + obj1.height) and (obj1.y <= obj2.y + obj2.width <= obj1.y + obj1.width)
    return cond1 or cond2
   
###############################################################################
class SpaceGame(window.Window):
    
    def __init__(self, *args, **kwargs):

        #Let all of the arguments pass through
        window.Window.__init__(self, *args, **kwargs)

        clock.schedule_interval(self.update, 1.0/30) # update at 30 H

        # setting text objects
        ft = font.load('Tahoma', 20)         #Create a font for our FPS clock
        self.fpstext = font.Text(ft, y=10)   # object to display the FPS
                               


        # loading image
        self.spaceship_image = pyglet.resource.image("ledMeme.png")
        self.spaceship = Spaceship(self.spaceship_image, x=200, y=50)
        self.game_on = True

    def update(self, dt):
        if not self.game_on:
            return

    def on_draw(self):
        self.clear() # clearing buffer
        clock.tick() # ticking the clock
        self.spaceship.image = self.spaceship_image
        
        if self.game_on:
            # showing FPS
            self.fpstext.text = "SCORE: %d" % 0
            self.fpstext.draw()
    
        # flipping
        self.flip()
    
    ## Event handlers
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')  
            
    def on_mouse_motion(self, x, y, dx, dy):
        self.spaceship.x = x
        #self.spaceship.y = y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
        
    def on_mouse_press(self, x, y, button, modifiers):
    	pass


####################################################################
class Spaceship(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
                  
###################################################################
  
if __name__ == "__main__":
    win = SpaceGame(caption="Aliens!! Invaders from Space!!", height=600, width=800)
    pyglet.app.run()