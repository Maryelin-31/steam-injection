# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 15:05:37 2023

@author: Maryelin
"""
from zml import *
from Utility.Chang7 import *
from Utility.Chang7.get_path import *

data = np.loadtxt(get_path('data.txt'))
# Translate the original data to near 0, and at the same time, 
# convert the original depth value into the positive direction of z up

y = data[:, 0]
y -= ((y[0] + y[1]) / 2)
y = [ i * (-1) if i < 0 else i for i in y]


# 0: z-coordinate
#1: Porosity
#2: Gas Saturation
#3: Water Saturation
#4: Light Oil Saturation
#5: Heavy Oil Saturation
#6: Kerogen Saturation


y2porosity = Interp1(x=y, y=data[:, 1])
y2sg = Interp1(x=y, y=data[:, 2])
y2sw = Interp1(x=y, y=data[:, 3])
y2slo = Interp1(x=y, y=data[:, 4])
y2sho = Interp1(x=y, y=data[:, 5])
y2sk = Interp1(x=y, y=data[:, 6])


