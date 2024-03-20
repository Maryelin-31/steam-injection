# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:26:37 2023

@author: Maryelin
"""

import numpy as np

def heat_c11h24(P, T):
    A = 195.647
    B = 0.9304
    C = -2.4683e-3
    D = 3.1735e-6
    
    CP = A + (B * T) + C * (T**2) + D * (T **3)
    return CP
