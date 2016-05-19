"""
atom.py

Describes the atom class for opticool.py
"""

from Tkinter import *
from constants import *
import math
import random


class Atom(object):
    def draw(self):
        # scales up the radius
        r = self.r * ENLARGE_ATOM * M_TO_PIX
        self.circle = self.context.screen.create_oval( int(round(self.x - (r/math.sqrt(2)) )), int(round(self.y - (r/math.sqrt(2)) )),int(round(self.x + (r/math.sqrt(2)) )),int(round(self.y + (r/math.sqrt(2)) )), fill = self.color)

    def destroy(self):
        self.context.screen.delete(self.circle)
    
    def interact(self,p):
        # sets the "last atom" of the photon
        p.lastatom = self
        if self.absorbs(p):
            self.r *= 1.05
            self.color = "white"
            # adjusts momentum/velocity
            self.vxy += H*BIG_PHOTON/p.l * math.cos(self.t-p.t) / self.m
            # stores photon and temporarily removes from context
            self.photons.append(p)
            self.context.killPhoton(p)
            self.context.after(int(round(TICK * HOLD_TICKS)), self.reemit)
        #else  :
        #    # reflects the photon
        #    p.t += math.pi

    def absorbs(self, p):
        # calculates the apparent frequency
        f = p.f * (p.V - self.vxy * math.cos(self.t-p.t))/C
        # checks if this frequency is within an absorptive band
        if ABS_MIN < f < ABS_MAX:
            return True
        return False

    def reemit(self):
        p = self.photons.pop()
        theta = random.random()*2*math.pi
        p.t = theta
        p.x = self.x + (self.r+2*p.V* M_TO_PIX * SLOW_LIGHT/S_TO_TICK)*math.cos(theta)
        p.y = self.y + (self.r+2*p.V* M_TO_PIX * SLOW_LIGHT/S_TO_TICK)*math.sin(theta)
        p.vx = p.V * M_TO_PIX * SLOW_LIGHT * math.cos(p.t) / S_TO_TICK
        p.vy = p.V * M_TO_PIX * SLOW_LIGHT * math.sin(p.t) / S_TO_TICK
        self.context.photons.append(p)
        self.color = "red"
        self.r /= 1.05


    def getTemp(self):
        return .5 * (self.k * pow(self.xy,2.) + self.m * pow(self.vxy,2)) / B
    

    def move(self):
        # remove old self
        self.destroy()
        # updates energy state
        if not self.photons:
            pass
        # calculate phase, position, and velocity with 10 sub-ticks
        i = 0
        self.vxy += -self.k * self.xy/(self.m*S_TO_TICK)
        self.xy += self.vxy / (S_TO_TICK) 
        self.x = self.x0 + self.xy * self.xcomp * M_TO_PIX
        self.y = self.y0 + self.xy * self.ycomp * M_TO_PIX
        # draws the circle
        self.draw()

    def __init__(self, context, x, y, temp0 = 290., frequency = MAG_F, radius = MAG_RAD, theta = 0, phase0 = 0, color = "red", mass = MAG_MASS): 
        # attributes for context, phase, base position, radius, frequency, theta, amplitude, mass, color
        self.context = context
        self.r = radius
        # mass
        self.m = float(mass)
        # oscillation frequency
        self.f = float(frequency)
        # visible radius
        self.R = radius * ENLARGE_ATOM * M_TO_PIX
        # visible coordinates central coordinates
        self.x0 = float(x)
        self.y0 = float(y)
        # spring constant
        self.k = pow(self.f*(2*math.pi),2.) * self.m
        self.t = float(theta)
        self.color = color
        self.photons = []
        # position and velocity
        self.xy = 0.
        self.vxy = math.sqrt(2*temp0*B/self.m)
        # simulates movement up to initial phase
        t0 = S_TO_TICK * random.random() / MAG_F
        t = 0
        while t < t0:
            self.vxy += -self.k * self.xy/(self.m*S_TO_TICK)
            self.xy += self.vxy / (S_TO_TICK) 
            t += 1
        # puts on screen!
        self.xcomp = math.cos(self.t)
        self.ycomp = math.sin(-self.t)
        # x and y pixel coordinates!
        self.x = self.x0 + (self.xy * self.xcomp) * M_TO_PIX
        self.y = self.y0 + (self.xy * self.ycomp) * M_TO_PIX
        # draws the circle
        self.draw()
