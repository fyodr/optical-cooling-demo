"""
photon.py

Describes the Pulse class for opticool.py using tkinter. 
"""

from Tkinter import *
from constants import *
import math
# undesirable patch for colission testing
import atom

class Pulse(object):
    def draw(self):
        i = 0
        self.segs = []
        wave = self.l*LONG_WAVES
        while i < int(round(wave)):
            x1 = self.x + int(round(self.ycomp*self.a*math.sin( (2.*math.pi/wave) * (i)) - self.xcomp*i ))
            y1 = self.y + int(round(-self.xcomp*self.a*math.sin( (2.*math.pi/wave) * (i)) - self.ycomp*i ))
            x2 = self.x + int(round(self.ycomp*self.a*math.sin( (2.*math.pi/wave) * (i+1)) - self.xcomp*i ))
            y2 = self.y + int(round(-self.xcomp*self.a*math.sin( (2.*math.pi/wave) * (i+1)) - self.ycomp*i ))
            self.segs.append(self.context.screen.create_line( x1,y1,x2,y2, fill = self.color ))
            i += 1
        head_radius = 1
        self.head = self.context.screen.create_oval(self.x-head_radius,self.y-head_radius,self.x + head_radius, self.y + head_radius, fill = "white")

    def destroy(self):
        while len(self.segs) > 0:        
            seg = self.segs.pop()
            self.context.screen.delete(seg)
        self.context.screen.delete(self.head)

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
        self.context = context
        self.V = C
        self.t = float(theta)
        self.xcomp = math.cos(self.t)
        self.ycomp = math.sin(self.t)
        # velocity in pixels per tick
        self.vx = self.V * M_TO_PIX * SLOW_LIGHT * self.xcomp / S_TO_TICK
        self.vy = self.V * M_TO_PIX * SLOW_LIGHT * self.ycomp / S_TO_TICK
        # pixel position
        self.x = x
        self.y = y
        self.f = float(frequency)
        self.l = float(self.V/self.f)
        self.a = self.l/2
        self.color = color
        self.lastatom = None
        if amplitude: self.a = float(amplitude)
        self.draw()
