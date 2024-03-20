# -*- coding: utf-8 -*-


from Utility.Chang7.get_path import *
from zmlx.alg.clamp import clamp
from saturation_data import *
from zml import *


def create_initial():
    """
    create initial field
    """

    def get_initial_t(x, y, z):
        """
        the initial temperature
        """
        return 338.0 + 22.15 - 0.0443 * y

    def get_initial_p(x, y, z):
        """
        the initial pressure
        """
        return 10e6 - 1e4 * y

    def get_perm(x, y, z):
        """
        the initial permeability
        """
        t = Tensor3()
        # t.xx = 1.0e-14
        # t.yy = 1.0e-15
        # t.zz = 1.0e-15
        return 1.0e-15

    def get_initial_s(x, y, z):
        """
        the initial saturation ()
        """
        # sg = y2sg(y)
        # assert sg >= 0, f'sg = {sg}'

        # sw = y2sw(y)
        # assert sw >= 0

        # slo = y2slo(y)
        # assert slo >= 0, f'slo = {slo}'

        # sho = y2sho(y)
        # assert sho >= 0, f'sho = {sho}'

        # sk = clamp(y2sk(y), 0, 0.7)  # 对最大值进行必要的限制，确保不是纯的固体
        # assert sk >= 0

        return (0, 0, 0), 0, 0, 0, (1.0, 0)
    
    
    def get_fai(x, y, z):
        """
        porosity
        """
        return 0.43

    def get_denc(x, y, z):
        """
        density * heat capacity
        """
        return 2600 * 1000

    def get_heat_cond(x, y, z):
        return 2.0

    return {'porosity': get_fai, 'pore_modulus': 100e6, 'p': get_initial_p,
            'temperature': get_initial_t,
            'denc': get_denc, 's': get_initial_s,
            'perm': get_perm, 'heat_cond': get_heat_cond, 'sample_dist': 0.01, 'dist': 0.01}


if __name__ == '__main__':
    print(create_initial())
