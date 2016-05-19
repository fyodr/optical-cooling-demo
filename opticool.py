"""
opticool.py

a program to model optical cooling.
"""
"""
cooltheatom.py

a game in which you cool an atom with a laser beam!
"""

##########################################################################
# Imports
from Tkinter import *            # Importing the Tkinter (tool box) library 
from constants import *
import math
import random
import photon
import atom
import coolbuttons
#import pyscreenshot as scrnsht


##########################################################################
# Main Class

class Opticool(Frame):

    def createWidgets(self):
        self.initScreen()
        self.buttons = coolbuttons.Buttons(self)
        self.buttons.pack()
    
    # makes the screen
    def initScreen(self):
        self.screen = Canvas(self, width = WIDTH, height = HEIGHT, background = BACKGROUND_COLOR)
        # adds the "trapped" atoms
        for i in range(A_PER_COL):
            for j in range(COL):
                self.addAtom(400 + j*2*HEIGHT/(A_PER_COL + 1), HEIGHT/(A_PER_COL*4) + i*HEIGHT/A_PER_COL+1 + (j%2)*HEIGHT/(2*(A_PER_COL)))
        self.screen.pack()

    def addPhoton(self, x, y, frequency, theta = 0, amplitude = 30, color = PHOTON_COLOR):
        self.photons.append( photon.Pulse(self, x, y, frequency, amplitude = amplitude, theta = theta, color = color) )

    def killPhoton(self,p):
        p.destroy()
        self.photons.remove(p)

    def addAtom(self, x, y, temp0 = 290., theta = 0, phase = 800, color = "red"):
        if phase == 800:
            phase = random.random()*S_TO_TICK/(MAG_F)
        if theta == 800:
            theta = 2 * math.pi * random.random()
        self.atoms.append( atom.Atom(self, x, y, temp0 = 290., frequency = MAG_F, radius = MAG_RAD, theta = theta, phase0 = phase, color = color))

    def getTemp(self):
        if hasattr(self,"temp"):    # ensures that self.temp exists
            count = 0
            temperature = 0.
            for a in self.atoms:
                count += 1
                temperature += a.getTemp()
            # temperature from energy, number of atoms and Boltzmann's Constant
            temperature = temperature / count
            self.temp.set("Temp = " + ("%.0f" % temperature) + "K")
        else :
            self.temp = StringVar()
            self.getTemp()

    def cleanPhotons(self):
        for p in self.photons:
            if p.x > WIDTH:
                self.killPhoton(p)
            elif p.y > HEIGHT:
                self.killPhoton(p)
            elif p.y < 0:
                self.killPhoton(p)
            elif p.x < -2:
                self.killPhoton(p)

    def update(self):
        if self.playing:
            # move all particles
            for p in self.photons:
                p.propogate()
            for a in self.atoms:
                a.move()
            # check for colissions
            #a = self.atoms[0]
            #for p in self.photons:
            #    if a.x - a.r < p.x and p.x < a.x + a.r:
            #        a.interact(p)
            # clean photons off of the back wall
            self.cleanPhotons()
        if self.atoms:    # guarantees that there is an atom
            self.getTemp()
        if self.autoplaying:
            if random.random() < FIRE_PERCENT:
                y = int(round(random.random()*WIDTH))
                self.addPhoton( 0, y, self.buttons.firingfreq, amplitude = 5, theta = 0 )
        self.after(TICK,self.update)
        
    def __init__(self, master = None):
        Frame.__init__(self,master)
        # makes constants accessible
        self.w = WIDTH
        self.h = HEIGHT
        self.TICK = TICK
        # pack
        self.pack()
        # adds lists for photons and atoms
        self.photons = []
        self.atoms = []
        # sets up display
        self.createWidgets()
        # starts updating
        self.after(TICK,self.update)

root = Tk()                   # Create a background window
root.wm_title("Optical Cooling")
o = Opticool(master = root)
o.mainloop()
