# -*- coding: utf-8 -*-


from zml import *


def create_interp(filename, ytimes=1.0):
    data = np.loadtxt(filename)
    x = data[:, 1]
    y = data[:, 0] * ytimes
    y[y < 0] = 0
    return Interp1(x=x, y=y)
