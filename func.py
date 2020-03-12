# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 17:52:47 2020

@author: User
"""


# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Fernanda Pinedo
# -- repositorio: https://github.com/ferpinedot/LAB_2_MFPT
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import numpy as np

# -- --------------------------------------------------- FUNCION: Leer archivo de entrada -- #
# -- ------------------------------------------------------------------------------------ -- #
# --
#%% 

def f_leer_archivo(param_archivo):
    """
    Parameters
    ----------
    param_archivo : str : nombre de archivo a leer
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    param_archivo = 'archivo_1_LNGO.xlsx'
    """

    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Sheet1')

    # Elegir solo reglones donde "type" == buy | sell
    # df_data.columns = [df_data[i] for i in range(len(df_data)) if df_data[i] == 'buy' or]

    # Convertir nombre de columnas en minusculas
    df_data.columns = [df_data.columns[i].lower() for i in list(df_data.columns)]

    # Asegurar que ciertas columnas son tipo numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
               'taxes', 'order']

    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)
    return df_data

#%%
    
# Para obtener el multiplicador expresando todo el pips
    
def f_pip_size(param_ins):
    """
    Parameters
    ----------
    param_ins : str : nombre de instrumento
    Returns
    -------
    Debugging
    """
    # encontar y eliminar un guion bajo
    inst = [param_ins.replace('-2', '') for i in ins]

    # transformar a minusculas
    inst = param_ins.lower()

    # lista de pips por instrumento
    pip_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                'chfjpy': 100,
                'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                'audusd': 10000, 'nzdusd': 10000, 'usdchf': 10000, 'eurgbp': 10000,
                'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000, 'gbpnzd': 10000,
                'gbpchf': 10000, 'gbpaud': 10000, 'audnzd': 10000, 'nzdcad': 10000,
                'audcad': 10000, 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pip_inst[inst]
    return

#%%

def f_columnas_datos(param_data):
    """

    :rtype: object
    """
    # convertir columna de 'closetime' y 'opentime' utilizando pd.to_datatime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] -
                             param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    return param_data['tiempo']

#%% 
def f_columnas_tiempos(param_data):
    """
    Parameters
    ----------
    param_data : DataFrame base
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    """
    # convertir columna de 'closetime' y 'opentime' utilizando pd.to_datatime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    return param_data['tiempo']
    return param_data


#%%

def f_columnas_pips(param_data):
    """
    Parameters
    ----------
    param_data : DataFrame base
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    """
#    param_data['pips'] = [param_data.loc[i,'closeprice'] * f_pip_size(param_ins=param_data.loc[i,'symbol']) for i in range\
#               (0, len(param_data.rows)) 
#                  if param_data['type'] == 'buy' else\
#                  param_data.loc[i,'openprice'] \
#                  * f_pip_size(param_ins=param_data.loc[i,'symbol'])]
#    return param_data['pips']
    
    return pd.DataFrame({
            'Operaciones totales': [len(datos['order']), 'Operaciones totales'],
            'Ops ganadoras': [len(datos['pip_acm']>=0, 'Operaciones ganadoras')]})


#%% 

#def f_stats_basic(datos):
    




