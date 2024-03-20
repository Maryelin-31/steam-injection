# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:33:06 2023

@author: Maryelin
"""

import numpy as np

def heat_c2h6(P, T):
    A = 38.332
    B = 0.4101
    C = -2.3024e-3
    D = 5.9347e-6
    
    CP = A + (B * T) + C * (T**2) + D * (T **3)
    return CP
