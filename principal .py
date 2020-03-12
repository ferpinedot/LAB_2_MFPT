# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 17:52:29 2020

@author: User
"""


# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Fernanda Pinedo
# -- repositorio: https://github.com/ferpinedot/LAB_2_MFPT
# -- ------------------------------------------------------------------------------------ -- #

import func as fn

#datos de entrada
#data_arch = 'archivo_mt4.xlsx'
data_arch = 'archivo_ejemplo.xlsx'

datos = fn.f_leer_archivo(data_arch)

fn.f_columnas_tiempos(datos)
fn.f_columnas_pips(datos)
stats = fn.f_stats_basic(datos)

#%%



#
#df_data = fn.f_columnas_tiempos(param_data = df_data)

#param_ins='usdjpy'
#fn.f_pip_size(param_ins)

#Pip size
pip_size = fn.f_pip_size(param_ins='eurusd')

#Tranformaciones de tiempo
datos = fn.f_columnas_tiempos(param_data=datos)

#Transformaciones Pips
datos = fn.f_columnas_pips(param_data=datos)