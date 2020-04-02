# -*- coding: utf-8 -*-
"""
Created on Thu Mar  26 17:34:22 2020

@author: User
"""

import matplotlib.pyplot as plt
import funciones as fn
import pandas as pd


datos = fn.f_leer_archivo(param_archivo='archivos/archivo_tradeview_1.xlsx', sheet_name= 0)

datos = fn.f_columnas_tiempos(datos)

# Número de pips
datos = fn.f_columnas_pips(datos)

# Capital acumulado ($)
datos = fn.f_capital_acm(datos)

profit_d = fn.f_profit_diario(datos)

profitd = profit_d.plot(x= 'timestamp' , y= 'profit_acm_d', kind = 'line')
plt.show()

# def rankin(datos):
#     """
#     Parameters
#     ----------
#     datos : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     None.

#     """
#     #rankin = df_1_ranking.plot(x='Índice', y = 'rank', kind = 'bar')
#     rankin = estadisticas['df_1_ranking'].plot(x='Índice', y = 'rank', kind = 'bar')
#     plt.show()



def profitd(datos):
    """
    Parameters
    ----------
    datos : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """ 
    profit_d.plot(x= 'timestamp' , y= 'profit_acm_d', kind = 'line')
    plt.show()
    
