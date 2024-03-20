# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 11:39:59 2023

@author: Maryelin
"""

import numpy as np
import matplotlib.pyplot as plt

def heat_c22h46(P, T):
    A = -69.933
    B =  4.8840
    C = -1.0197e-2
    D =  8.0828e-6
    
    CP = A + (B * T) + C * (T**2) + D * (T **3)
    return CP

# T = np.linspace(300,200, 100)
# P = np.linspace(1.0e6, 40.0e6,100)

# heat = []
# for t in T:
#     for p in P:
#         print(heat_c22h46(p, t))
#         heat.append(heat_c22h46(p, t))

# heat = np.array(heat)
# heat= np.transpose(heat.reshape((heat.size // 100, 100)))
# plot = plt.contourf(heat, 20, extent=[T.min(), T.max(), P.min(), P.max()] ,cmap='coolwarm')
        
