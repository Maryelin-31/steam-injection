# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:33:46 2023

@author: Maryelin
"""
import numpy as np

def heat_methane(P, T):
    A = -0.018
    B = 1.1982
    C = -9.8722e-3
    D = 3.1670e-5
    
    CP = A + (B * T) + C * (T**2) + D * (T **3)
    return CP
