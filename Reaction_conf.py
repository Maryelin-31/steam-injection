# -*- coding: utf-8 -*-


from zml import Interp1, create_dict, ConjugateGradientSolver, Seepage, version
from zmlx.fluid import *
from zmlx.fluid.conf import *
from zmlx.config.TherFlowConfig import TherFlowConfig
from zmlx.fluid.kerogen import create as create_kerogen
from zmlx.fluid.h2o_gas import create as create_h2o_gas
from zmlx.fluid.h2o import create as create_h2o
from zmlx.fluid.char import create as create_char
from zmlx.fluid.ch4_lyx import create as create_methane_gas
from zmlx.fluid.conf.gas_mixture import Gas_mixture


from zmlx.kr.create_krf import create_krf
from zmlx.react import decomposition
from zmlx.react import vapor as vapor_react


def create():
    """
    Braun and Burhan, 1993
    the gas is asume as a mixture of gas, 
    the methane appears when the gas mixture is cracking
    this author does not considers the water reaction. 
    
    create the vapor reaction in the injection well
    """
    config = TherFlowConfig()
    
    # Gas Phase (gas mixture, methane, steam_water())
    config.iGAS = config.add_fluid([Gas_mixture(), create_methane_gas(), create_h2o_gas()])
    
    # Water
    config.iwat = config.add_fluid(create_h2o())
    
    #Light Oil
    config.iLO = config.add_fluid(create_light_oil_liq())
    
    # Heavy Oil
    config.iHO = config.add_fluid(create_heavy_oil_liq())

    # Solid phase Kerogen
    config.isol = config.add_fluid([create_kerogen(), create_char()])
    
    # h2o and steam
    config.reactions.append(
        vapor_react.create(
            vap=(config.iGAS, 2),
            wat=config.iwat,
            fa_t=config.flu_keys['temperature'],
            fa_c=config.flu_keys['specific_heat']))
    
    # The decomposition of Kerogen.
    config.reactions.append(
        decomposition.create(left=(config.isol, 0), right=[(config.iHO, 0.6), 
                                                               (config.iLO, 0.1),
                                                               (config.iLO, 0.05),
                                                               ((config.iGAS, 0), 0.05),
                                                               ((config.isol, 1), 0.2),
                                                               ],
                             temp=563.15, heat=161100.0, 
                             rate=4.81e-6,
                             fa_t=config.flu_keys['temperature'],
                             fa_c=config.flu_keys['specific_heat']))

    # The decomposition of Heavy oil
    config.reactions.append(
        decomposition.create(left=config.iHO, right=[(config.iLO, 0.5),   
                                                         ((config.iGAS, 0), 0.2),
                                                         ((config.isol, 1), 0.3),
                                                         ],
                             temp=623.15, heat=219328.0, 
                             rate=2.71e-7,
                             fa_t=config.flu_keys['temperature'],
                             fa_c=config.flu_keys['specific_heat']))
    
    # The decomposition of Light Oil
    # config.reactions.append(
    #     decomposition.create(index=config.iLO, iweights=[((config.iGAS, 0), 0.703),
    #                                                       ((config.isol, 1), 0.297),
    #                                                       ],
    #                           temp=873.15, heat=219328.0, 
    #                           rate=1.0e-8,
    #                           fa_t=config.flu_keys['temperature'],
    #                           fa_c=config.flu_keys['specific_heat']))
    
    # # The decomposition of Gas
    # config.reactions.append(
    #     decomposition.create(index=(config.iGAS, 0), iweights=[((config.iGAS, 1), 0.687),
    #                                                             ((config.isol, 1), 0.313),
    #                                                           ],
    #                           temp=633.15, heat=238488.0, 
    #                           rate=2.53e-8,
    #                           fa_t=config.flu_keys['temperature'],
    #                           fa_c=config.flu_keys['specific_heat']))

    return config


if __name__ == '__main__':
    c = create()

