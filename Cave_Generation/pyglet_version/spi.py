#!/usr/bin/env python
#extended version of tutorial in pyglet http://www.meetup.com/PyLadies-Berlin/events/211277902/ 

import random, math
import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font
from pyglet.window import key 

                          
def collision(obj1, obj2):
    cond1 = (obj1.x <= obj2.x <= obj1.x + obj1.height) and (obj1.y <= obj2.y <= obj1.y + obj1.width)
    cond2 = (obj1.x <= obj2.x + obj2.height <= obj1.x + obj1.height) and (obj1.y <= obj2.y + obj2.width <= obj1.y + obj1.width)
    return cond1 or cond2
   
###############################################################################
class SpaceGame(window.Window):
    
    def __init__(self, *args, **kwargs):

        #Let all of the arguments pass through
        window.Window.__init__(self, *args, **kwargs)
        

        self.game_over_screen = pyglet.text.Label('Game Over', font_size=36,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center', multiline=True, 
                          width=self.width//2)
        clock.schedule_interval(self.update, 1.0/30) # update at 30 H
        clock.schedule_interval(self.create_alien, 0.5) # update at 30 Hz
        # setting text objects
        ft = font.load('Tahoma', 20)         #Create a font for our FPS clock
        self.fpstext = font.Text(ft, y=10)   # object to display the FPS
        self.livestext = font.Text(ft, x=self.width, y=self.height, 
                               halign=pyglet.font.Text.RIGHT, 
                               valign=pyglet.font.Text.TOP)
                               


        # loading image
        self.spaceship_image = pyglet.image.load('../resources/ledMeme.png')
        self.spaceship = Spaceship(self.spaceship_image, x=200, y=50)
        self.spaceship_burning_image = pyglet.image.load('../resources/ledMeme.png')
        #self.burning_spaceship = Spaceship(, x=200, y=50)
        
        
        self.alien_image = pyglet.image.load('../resources/ledMeme.png')
        self.aliens = []
        
        self.bullet_image = pyglet.image.load('../resources/ledMeme.png')
        self.bullets = []
        self.score = 0
        self.on_explosion = 0
        self.lives = 5
        self.game_on = True

    def update(self, dt):
        if not self.game_on:
            return
        
        for alien in self.aliens:
            alien.update()
            if alien.dead:
                self.aliens.remove(alien)
        for bullet in self.bullets:
            bullet.update()
            if bullet.dead:
                self.bullets.remove(bullet)
                
        for alien in self.aliens:
            for bullet in self.bullets:
                if collision(alien, bullet):
                    self.bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.score += 1

        for alien in self.aliens:
            if collision(alien, self.spaceship):
                self.aliens.remove(alien)
                self.lives -= 1
                self.on_explosion = 20
        
        if self.lives <= 0 and self.on_explosion <=0:
            self.game_on = False
                             
    
    def create_alien(self, dt):
        speed_boost = self.score / 5
        self.aliens.append(Alien(speed_boost, self.alien_image, x=random.randint(0,self.width), y=self.height))

    def on_draw(self):
        self.clear() # clearing buffer
        clock.tick() # ticking the clock
        self.spaceship.image = self.spaceship_image
        if self.on_explosion > 0:
            if self.on_explosion % 4:
                self.spaceship.image = self.spaceship_burning_image
            self.on_explosion -= 1            
        
        if self.game_on:
            # showing FPS
            self.fpstext.text = "SCORE: %d" % self.score
            self.fpstext.draw()
            
            self.livestext.text = "LIVES: %d" % self.lives
            self.livestext.draw()
            self.spaceship.draw()
            for alien in self.aliens:
                alien.draw()
            for bullet in self.bullets:
                bullet.draw()
            
        else:
            self.game_over_screen.text = "GAME OVER\nscore: %d" % self.score
            self.game_over_screen.draw()
    
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
        self.bullets.append(Bullet(self.height, self.bullet_image, x=self.spaceship.x + 20, y=self.spaceship.y + 30))



####################################################################
class Spaceship(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
     
        
####################################################################
class Alien(pyglet.sprite.Sprite):

    def __init__(self, speed_boost, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)   
        self.x_velocity= random.randint(-3,3)
        self.y_velocity= 5 + speed_boost
        self.dead = False
        
    def update(self):
        self.x -= self.x_velocity
        self.y -= self.y_velocity
        if self.y < 0 or self.x < 0:
            self.dead = True

class Bullet(pyglet.sprite.Sprite):

    def __init__(self, max_height, *args, **kwargs):
        self.max_height = max_height
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)   
        self.y_velocity= 5
        self.dead = False
        
    def update(self):
        self.y += self.y_velocity
        if self.y > self.max_height:
            self.dead = True
                  
###################################################################
  
if __name__ == "__main__":
    win = SpaceGame(caption="Aliens!! Invaders from Space!!", height=600, width=800)
    pyglet.app.run()