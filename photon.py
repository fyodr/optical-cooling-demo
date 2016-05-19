"""
photon.py
by Ted Morin

Describes the Pulse (photon) class for optical cooling demo using tkinter. 
"""

# imports
from Tkinter import *           #TODO turn this into "import Tkinter as tk" and check code
from constants import *
import math

class Pulse(object):
    
    # draws in a sine wave of wavelength equal to the photon's wavelength, scaled by LONG_WAVES
    def draw(self):
        i = 0                           # counter for number of segments
        self.segs = []                      
        wave = self.l*LONG_WAVES
        while i < int(round(wave)):    
                # the endpoints of each segment are calculated and drawn
                # TODO replace with a faster method from tk? Does one exist?
            x1 = self.x + int(round(self.ycomp*self.a*math.sin( (2.*math.pi/wave) * (i)) - self.xcomp*i ))
            y1 = self.y + int(round(-self.xcomp*self.a*math.sin( (2.*math.pi/wave) * (i)) - self.ycomp*i ))
            x2 = self.x + int(round(self.ycomp*self.a*math.sin( (2.*math.pi/wave) * (i+1)) - self.xcomp*i ))
            y2 = self.y + int(round(-self.xcomp*self.a*math.sin( (2.*math.pi/wave) * (i+1)) - self.ycomp*i ))
            self.segs.append(self.context.screen.create_line( x1,y1,x2,y2, fill = self.color ))
            i += 1                      # each segment corresponds to 1 pixel
        # shows the actual location of the photon as a point
        head_radius = 1         # radius of the photon's location indicator is 1. TODO remove create_oval?
        self.head = self.context.screen.create_oval(self.x-head_radius,self.y-head_radius,self.x + head_radius, self.y + head_radius, fill = "white")

    # removes the photon's parts from the screen
    def destroy(self):
        # removes the segments
        while len(self.segs) > 0:               #TODO replace this if the sine drawing is improved
            seg = self.segs.pop()
            self.context.screen.delete(seg)
        # removes the location indicator
        self.context.screen.delete(self.head)

    # moves the photon in its direction of propogation
    def propogate(self):
        # remove segments and head of this pulse
        while len(self.segs) > 0:        
            seg = self.segs.pop()
            self.context.screen.delete(seg)
        self.context.screen.delete(self.head)
        # calculates new x and y
        self.x += self.vx
        self.y += self.vy
        # checks for collisions with atoms
        for a in self.context.atoms:
            if abs(a.x - self.x) < a.R and abs(a.y - self.y) < a.R:                                                 # broadly checks x and y bounds
                if math.sqrt(math.pow(self.x-a.x,2)+math.pow(self.y-a.y,2)) < a.R and a is not self.lastatom:       # checks with proper distance and prevents doubles
                    a.interact(self)
                return
        self.draw()

    def __init__(self, context, x, y, frequency, theta = 0, amplitude = 0, color = "violet"):
        self.context = context              # identifies the context in which visible components will exist
        self.V = C                          # identifies the speed of light TODO ensure this is necessary?
        self.t = float(theta)               # documents the angle at which the photon moves
        self.xcomp = math.cos(self.t)       # stores the x-component of the photons Poynting vector
        self.ycomp = math.sin(self.t)       # stores the y-component of the photons Poynting vector
        self.vx = self.V * M_TO_PIX * SLOW_LIGHT * self.xcomp / S_TO_TICK   # calculates x-velocity in pixels per tick
        self.vy = self.V * M_TO_PIX * SLOW_LIGHT * self.ycomp / S_TO_TICK   # calculates x-velocity in pixels per tick
        self.x = x                          # initial x (pixels)
        self.y = y                          # initial y (pixels)
        self.f = float(frequency)           # stores frequency and ensures that frequency is a float
        self.l = float(self.V/self.f)       # stores the wavelength and ensure that it is a float
        self.a = .5 * self.l                        # default amplitude = .5 * wavelength
        if amplitude: self.a = float(amplitude)     # inserts amplitude if given
        self.color = color                  # color of the lightwave
        self.lastatom = None                # a pointer to whichever atom the photon struck last
        self.draw()
