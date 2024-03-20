# -*- coding: utf-8 -*-
"""

@author: Maryelin

STEAM FLOOD INJECTION
"""

# from zml_hyd import 

"""
install in console 
pip install chemicals 
pip install pyXSteam
"""

from zml import *
from zmlx.alg import make_fname
from zml import Interp1, create_dict, ConjugateGradientSolver, Seepage, version

import matplotlib.tri as tri
from matplotlib import pyplot as pyplot
from matplotlib.cm import ScalarMappable
from zmlx.utility.SeepageNumpy import as_numpy
import numpy as np
import os

from mesh import *
from Reaction_conf import create
from initial_cond import *

from zmlx.kr.create_krf import create_krf
from zmlx.alg.linspace import linspace
from zmlx.utility.HeatInjector import HeatInjector
from zmlx.utility.RelativePermeability import stone_model_II

"following Profesor Workspace"

def seepage_script(rate_inj):

    "Create Mesh"
    mesh = create_mesh()
    # print(mesh)
        
    config = create()
    
    "Initial Conditions Reservoir"
    ini = create_initial()
    
    "create model"
    model = config.create(mesh, **ini)  # create
    model.set(gravity=(0, -10, 0))
    
    
    "relative permeability"
    # sw, krw, sg, krg, so, kro = stone_model_II(swi = 0.05, sgc = 0.05, sorw = 0.005, sorg = 0.005, 
    #                                             krowe = 0.85, krwe = 0.4, kroge = 0.85, krge = 3, 
    #                                             nsorw = 3, nw = 3, nog = 3, ng = 3)
    
    # model.set_kr(config.iGAS, sg, krg)
    # model.set_kr(config.iwat, sw, krw)
    # model.set_kr(config.iLO,  so, kro)
    # model.set_kr(config.iHO,  so, kro)
    
    
    model.set_kr(config.iGAS, *create_krf(0.05, 3.0))
    model.set_kr(config.iwat, *create_krf(0.05, 3.0))
    model.set_kr(config.iLO, *create_krf(0.05, 3.0))
    model.set_kr(config.iHO, *create_krf(0.05, 3.0))

    # for face in model.faces:
    #     pos = face.get_cell(0).pos
    #     pressure = ini['p'](*pos)
    #     print(pressure)
    
    
    "Production Well"
    
    pos = (15.0, 8.0, 1000)
    cell = model.get_nearest_cell(pos=pos)
    x, y, z = cell.pos
    virtual_cell = config.add_cell(model, vol=cell.get_attr(config.cell_keys['vol']), pos=pos, porosity=1.0e3, pore_modulus=20e6,
                                   temperature=ini['temperature'](*pos), p=1.0e6,
                                   s=ini['s'](*pos))
    
    face = config.add_face(model, virtual_cell, model.get_cell(cell.index),
                           heat_cond=0, perm=1e-14, area=3.0, length=1.0, )
    
    prectrl = PressureController(virtual_cell, t=[0, 1e10], p=[1e6, 1e6])
    monitor = SeepageCellMonitor(get_t=lambda: config.get_time(model),
                                  cell=(virtual_cell, prectrl))
    

    "Injection Configuration"
    cell_ids = set()

    z = 0
    y = 5.0
    for x in (10.0, 20.0):
        cell = model.get_nearest_cell(pos=(x, y, z))
        cell_ids.add(cell.index)

    # Add_injector
    for cell_id in cell_ids:
        cell1 = model.get_cell(cell_id)
        flu = cell1.get_fluid(0).get_component(2)  # Steam
        flu.set_attr(config.flu_keys['temperature'], 500)
        injector = model.add_injector(cell=cell1, fluid_id=[0, 2], flu=flu,
                           pos=cell1.pos, radi=3.0, opers=[(0, rate_inj)])
    
    "Time step Strategy"
    config.set_dv_relative(model, 0.5)  # The ratio of the distance traveled by each time step to the grid size
    config.set_dt(model, 0.01)  # initial value for time step
    config.set_dt_max(model, 24 * 3600 * 7)  # Maximum value of time step <one week> # Maximum value of time step <one week>
    config.set_dt_min(model, 3600)  # Minimum step size is 1 hour
    
    "Save Results"
     
    def cell_mass(cell):
        fluid = []
        total = []
        for i in range(cell.fluid_number):
            total.append(cell.get_fluid(i).mass)
            if cell.get_fluid(i).component_number == 0:
                fluid.append(cell.get_fluid(i).mass)
            else:
                for j in range(cell.get_fluid(i).component_number):
                    fluid.append(cell.get_fluid(i).get_component(j).mass)
        saturation = [i / sum(total) for i in fluid]
        return saturation
    
    def fluid_sat(cell):
        fluid = []
        for i in range(cell.fluid_number):
            if cell.get_fluid(i).component_number == 0:
                fluid.append(cell.get_fluid(i).vol_fraction)
            else:
                for j in range(cell.get_fluid(i).component_number):
                    fluid.append(cell.get_fluid(i).vol_fraction)
        return fluid
    
    def save_sat(path):
        result_folder = os.path.join(os.getcwd(), 'data', f'Results_rate_{rate_inj}', 'Saturation_cells')
        
        if os.path.exists(f'result_folder'):
            import shutil
            shutil.rmtree(f'result_folder')            
        os.makedirs(result_folder, exist_ok=True)
        
        SavePath = os.path.join(result_folder, path)
        with open(SavePath, 'w') as file:
            for cell in model.cells:
                x, y, z = cell.pos
                satu = fluid_sat(cell)
                satu_str = ' '.join(str(i) for i in satu)
                file.write(f'{x} {y} {z} {satu_str}\n')
       
    def save_mass(path):
        result_folder = os.path.join(os.getcwd(), 'data', f'Results_rate_{rate_inj}', 'Results_cells')
        
        if os.path.exists(f'result_folder'):
            import shutil
            shutil.rmtree(f'result_folder')            
        os.makedirs(result_folder, exist_ok=True)
        
        SavePath = os.path.join(result_folder, path)
        with open(SavePath, 'w') as file:
            for cell in model.cells:
                x, y, z = cell.pos
                temp = cell.get_attr(config.cell_keys['temperature'])
                pres = cell.get_attr(config.cell_keys['pre'])
                file.write(f'{x} {y} {z} '
                           f'{cell.get_fluid(0).get_component(0).mass} {cell.get_fluid(0).get_component(1).mass} {cell.get_fluid(0).get_component(2).mass} '
                           f'{cell.get_fluid(1).mass} '
                           f'{cell.get_fluid(2).mass} '
                           f'{cell.get_fluid(3).mass} '
                           f'{cell.get_fluid(4).get_component(0).mass} {cell.get_fluid(4).get_component(1).mass} '
                           f'{temp} {pres}\n')
    
    
    def run():
        data_path = os.path.join(os.getcwd(), 'data')
        resu_path = os.path.join(data_path, f'Results_rate_{rate_inj}')
        os.makedirs(os.path.join(os.getcwd(), 'data', f'Results_rate_{rate_inj}'), exist_ok=True)
        # folder = os.getcwd()
        folder = os.path.join(os.getcwd(), 'data', f'Results_rate_{rate_inj}')
        
        
        solver = ConjugateGradientSolver()
        solver.set_tolerance(1.0e-13)
        
        prei = 10e6
        kini = 1.0e-15
        cfr= 0.05e-6

        for step in range(1000000):
            config.iterate(model, solver=solver)
            time = config.get_time(model)
            

            "Permeability vs Pressure"
            # if step % 100 == 0:

                # for face in model.faces:
                #     pre = (face.get_cell(0).pre + face.get_cell(1).pre) / 2
                #     dp = prei - pre
                #     perm= kini * (1 - cfr * (dp))**3
                #     face.set_attr(config.face_keys['perm'], perm)
                #     cond= perm * (face.get_attr(config.face_keys['area']) / face.get_attr(config.face_keys['length']))
                #     face.set_attr(config.face_keys['g0'], cond)

                    
            # HeatCapacity Abdelagatov, 2021 base on Wittington, 2009
            for cell in model.cells:
                vol = cell.get_attr(config.cell_keys['vol'])
                temp = cell.get_attr(config.cell_keys['temperature'])
                heat_cap = (0.849315 + 0.000565 * temp - 25002.318124 * temp ** (-2)) * 1000
                cell.set_attr(config.cell_keys['mc'], vol * 2600 * heat_cap)
    
            # Heat Conductivity Jin et al, 2022 (experiment)
            ca_t = config.cell_keys['temperature']
            fa_g = config.face_keys['g_heat']
            for face in model.faces:
                temp = (face.get_cell(0).get_attr(ca_t) + face.get_cell(1).get_attr(ca_t)) / 2
                heat_con = (-0.0006 * temp) + 0.8126
                face.set_attr(fa_g, heat_con)
    
            if config.get_time(model) > 3600 * 24 * 365 * 3:
                print(f'{step}, Finish')
                break
            
            path = f'time_{time}.txt'
            if step % 100 == 0:
                save_mass(path)
                save_sat(path)
                monitor.update(dt=config.get_dt(model))
                monitor.save(os.path.join(folder, 'prod.txt'))
                print(f'{step} {time / (3600 * 24)}')
                    
    
    run()
    # 
    
seepage_script(rate_inj=0.0001)
