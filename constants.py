"""
constants.py

constants for opticool and cooltheatom
"""

################################################################
# REAL constants

# Planck's Constant
H = 6.62607e-34
# Boltzmann's Constant (J/K)
B = 1.38065e-23
# specific heat of each atom
K = 2 * B
# speed of light
C = 3e8
# density of magnesium (atoms per m^3)
D = 2e13
# absorption wavelength (meters)
MAG_ABS = 2.852e-7


# radius of a magnesium atom
MAG_RAD = 1.45e-10
# mass of a magnesium atom (in kg
MAG_MASS = (24.305/1000)/6.02214e23
# frequency of magnesium atom
MAG_F = 200000.

##################################################################
# conversion constants

# for opticool: 
# The radius of the atom (scaled up by 1,000,000) should be 20 pixels. The amplitude should not exceed 3 times (scaled) r.
# Light (scaled) should travel at 4 pixels per tick.

# 1 = 137931. pixel / meter
M_TO_PIX = 137931.
# 1 = 1.93333E-6 seconds / TICK
S_TO_TICK = 1.0344825e8
# 1 = 1,000,000 gameR / R (radius of atoms is scaled up in the game, for collisions and drawing)
ENLARGE_ATOM = 1000000.
# 1 = 100,000 gameC / c  (speed of light is scaled down in the game. scale back up for doppler!)
SLOW_LIGHT = 1/100000.
# 1 = .075 PIX / wavelength-nm (wavelengths are adjusted so that they are visible, and vary visibly over the spectrum shown.
LONG_WAVES = .075*1e9
# 1 = 10GameH/H (where H is planck's constant)
BIG_PHOTON = 20


##################################################################
# "game" constants

# tick length
TICK = 20 #milliseconds
# dimensions of the screen
WIDTH = 640
HEIGHT = 480

# atoms per column
A_PER_COL = 9
# columns of atoms
COL = 3

# Percent chance of a photon firing per tick
FIRE_PERCENT = .6

# background of screen
BACKGROUND_COLOR = "black"

# photon color
PHOTON_COLOR = "red"

###################################################
# Slider constants (in nanometers)
# LAMBSLIDEr min
LAMBSLIDE_MIN = 2900000.
# LAMBSLIDEr max
LAMBSLIDE_MAX = 2800000.
# default LAMBSLIDEr setting
LAMBSLIDE_DEFAULT = 2862001.
# LAMBSLIDEr Modifier (puts lambda in terms of tenths of nanometers)
LAMBSlideMod = 1e-13
# LAMBSLIDEr Length
LAMBSLIDE_LEN = 150

#minimum frequency for absorption (in terms of lambda)
ABS_MIN = C / (2.852e-7 + 1e-9)
#maximum frequency for absorption (in terms of lambda)
ABS_MAX = C / (2.852e-7 - 1e-9)

# Photon hold time: time before absorbed photons are reemited (in TICKs)
HOLD_TICKS = 10.
