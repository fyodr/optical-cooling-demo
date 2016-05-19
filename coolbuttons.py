"""
optibuttons.py

Describes the controller widget for cooltheatom
"""

from Tkinter import *            # Importing the Tkinter (tool box) library 
from constants import *
import math
import random

class Buttons(Frame):

    def __init__(self,master):
        Frame.__init__(self,master = master)
        master.playing = True
        def playcallback():
            if master.playing:
                master.playing = False
                master.play.config(text = "Play")
            else :
                master.playing = True
                master.play.config(text = "Pause")
        master.play = Button(self,text = "Pause", width = 5, command = playcallback)
        master.play.pack(side = LEFT)

        # sets firing frequency and wavelength from slider
        def slidecallback(lamb):
            if hasattr(self,"slidelabeltxt"):  # ensures that variables exist
                lamb = float(lamb)
                self.firingfreq = C/(lamb*LAMBSlideMod)
                self.firinglamb = lamb*LAMBSlideMod
                self.slidelabeltxt.set(format(self.firinglamb*1e9,'.4f') + "nm (" + format(self.firingfreq*1e-9,'.1f') + "GHz)")
            else :
                self.slidelabeltxt = StringVar()
                slidecallback(lamb)
        slidecallback(LAMBSLIDE_DEFAULT)
        # controls firing frequency and wavelength
        self.LAMBSlider = Scale(self, orient = HORIZONTAL, length = LAMBSLIDE_LEN, takefocus = 1, showvalue = 0, from_ = LAMBSLIDE_MIN, to = LAMBSLIDE_MAX, command = slidecallback)
        self.LAMBSlider.set(LAMBSLIDE_DEFAULT)
        self.LAMBSlider.pack(side = LEFT)
        # displays firing frequency and wavelength
        self.SlideLabel = Label(self,textvariable = self.slidelabeltxt, justify = LEFT)
        self.SlideLabel.pack(side = LEFT)

        # fires a photon!
        def firecallback():
            self.master.addPhoton( 0, HEIGHT/2, self.firingfreq, amplitude = 5, theta = 0 )
        self.fire = Button(self,text = "Fire!", width = 5, command = firecallback)
        self.fire.pack(side = LEFT)
        # initiates autoplay
        master.autoplaying = False
        def autoplaycallback():
            if master.autoplaying:
                master.autoplaying = False
                master.autoplay.config(text = "Auto")
            else :
                master.autoplaying = True
                master.autoplay.config(text = "Stop")
        master.autoplay = Button(self,text = "Auto", width = 5, command = autoplaycallback)
        master.autoplay.pack(side = LEFT)

        # displays the temperature 
        self.master.getTemp()
        self.tempLabel = Label(self,textvariable = self.master.temp, justify = LEFT)
        self.tempLabel.pack(side = LEFT)
