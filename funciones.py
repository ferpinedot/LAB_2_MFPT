# -- coding: utf-8 --
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

#%% Parte 2: Mediciones estadísticas básicas
#%%
# Lectura del archivo de datos en excel o csv

def f_leer_archivo(param_archivo, sheet_name = 0):
    """
    Parameters
    ----------
    param_archivo : str : nombre de archivo a leer
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    
    Debugging
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'
    """

    #df_data = pd.read_csv(param_archivo)
    df_data = pd.read_excel(param_archivo, sheet_name = 0)
    df_data.columns = [i.lower() for i in list(df_data.columns)]
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)
    return df_data
#%%
    
# Para obtener el multiplicador expresando todo el pips
# Número de pips por instrumento

def f_pip_size(param_ins):
    """
    Parameters
    ----------
    param_ins : str : nombre de instrumento
    
    Returns
    -------
    pip_inst : func : valor en pips del instrumento seleccionado
    
    Debugging
    ---------
    
    """
    
    # encontar y eliminar un guion bajo
    # inst = [param_ins.replace('-2', '') for i in ins]

    # transformar a minúsculas
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
    #return

#%%
# Columna tiempo agregada para saber el tiempo transcurrido de una operación

def f_columnas_tiempos(param_data):
    """
    Parameters
    ----------
    param_data : pd.DataFrame : df con información de transacciones ejecutadas
    
    Returns
    -------
    param_data : pd.DataFrame : df con columna agregada 'tiempo'
    
    Debugging
    ---------
    param_data = f_leer_archivo("archivo_tradeview_1.xlsx")
    """
    
    # convertir columnas de 'closetime' y 'opentime' utilizando pd.to_datatime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] -
                             param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    # return param_data['tiempo']
    return param_data

#%%
# Nuevas columnas pips para saber el tamaño en pips de las transacciones ejecutadas 

def f_columnas_pips(datos):
    """
    Parameters
    ----------
    datos : pd.DataFrame : dataframe con las transacciones ejecutadas ya con la columna 'tiempos'

    Returns
    -------
    param_data : pd.DataFrame : dataframe anterior pero con columnas 'pips' y 'pips acumulados'
    
    Debugging
    ---------
    datos =  f_leer_archivo("archivo_tradeview_1.xlsx")
    
    """
#    param_data['pips'] = [param_data.loc[i,'closeprice'] * f_pip_size(param_ins=param_data.loc[i,'symbol']) for i in range\
#               (0, len(param_data.rows)) 
#                  if param_data['type'] == 'buy' else\
#                  param_data.loc[i,'openprice'] \
#                  * f_pip_size(param_ins=param_data.loc[i,'symbol'])]
#    return param_data['pips']
    
    datos['pips'] = [(datos.closeprice[i] - datos.openprice[i])*f_pip_size(datos.symbol[i]) for i in range(len(datos))]
    datos['pips'][datos.type == 'sell'] *= -1
    datos['pips_acm'] = datos.pips.cumsum()
    datos['profit_acm'] = datos['profit'].cumsum()
    
    return datos.copy()

#%%  Estadísticas básicas

def f_basic_stats(datos):
    """
    Parameters
    ----------
      datos : pd.DataFrame : dataframe con las transacciones ejecutadas, después de 'tiempos'
    
    Returns
    -------
    Dos dataframes:
    df_1_tabla : pd.DataFrame : dataframe con estadísticas básicas del comportamiento del trader
    df_2_ranking : pd.DataFrame : dataframe con un ranking entre el 0 y el 1 en donde se califica con cuales divisas se obtuvieron operaciones precisas realizadas
        
    Debugging
    ---------
    datos = f_leer_archivo("archivo_tradeview_1.xlsx")
    """
    # print('------------')
    # print(datos.head(3))
    # print('------------')
    
    # Ejemplo: df[(df['col1'] >= 1) & (df['col1'] <=1 )]
    
    df_1_tabla = pd.DataFrame({'Ops totales': [len(datos['order']), 'Operaciones totales'],
                                'Ops ganadoras': [len(datos[datos['profit'] >= 0]), 'Operaciones ganadoras'],
                                'Ops ganadoras_b': [len(datos[(datos['type'] == 'buy') & (datos['profit'] >= 0)]), 'Operaciones ganadoras en compra'],
                                'Ops ganadoras_s': [len(datos[(datos['type'] == 'sell') & (datos['profit'] >= 0)]), 'Operaciones ganadoras en venta'],
                                'Ops perdedoras': [len(datos[datos['profit'] < 0]), 'Operaciones perdedoras'],
                                'Ops perdedoras_b': [len(datos[(datos['type'] == 'buy') & (datos['profit'] < 0)]), 'Operaciones perdedoras en compra'],
                                'Ops perdedoras_s' : [len(datos[(datos['type'] == 'sell') & (datos['profit'] < 0)]), 'Operaciones perdedoras en venta'],
                                'Profit media': [datos['profit'].median(), 'Mediana de profit de operaciones'],
                                'Pips media': [datos['pips'].median(), 'Mediana de pips de operaciones'],
                                'r_efectividad': [len(datos[datos['profit'] >= 0])/len(datos['order']), 'Ganadoras Totales/Operaciones Totales'],
                                'r_proporcion': [len(datos[datos['profit'] >= 0]) / len(datos[datos['profit'] < 0]), 'Perdedoras Totales/Ganadoras Totales'],
                                'r_efectividad_b': [len(datos[(datos['type'] == 'buy') & (datos['profit'] >= 0)]) / len(datos['order']), 'Operaciones ganadoras de compra/Operaciones Totales'],
                                'r_efectividad_s': [len(datos[(datos['type'] == 'sell') & (datos['profit'] >= 0)]) / len(datos['order']), 'Operaciones ganadoras de venta/Operaciones Totales'],
                                }, index = ['Valor', 'Descripción']).transpose()
    
    tb1 = pd.DataFrame({i: len(datos[datos.profit >0][datos.symbol == i])/len(datos[datos.symbol == i])
                        for i in datos.symbol.unique()}, index = ['rank']).transpose()
    
    df_1_ranking = (tb1*100).sort_values(by = 'rank', ascending = False).T.transpose()
    
    return {'df_1_tabla' : df_1_tabla.copy(), 'df_1_ranking' : df_1_ranking.copy()}

#%% Parte 3: Medidas de atribución al desempeño
#%% 
# Cálculo del capital acumulado
def f_capital_acm(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : dataframe con transacciones ejecutadas después de haber corrido 'tiempos' y 'pips'

    Returns
    -------
    datos : pandas.DataFrame : se le agrega una columna al dataframe
    
    Debugging
    ---------
    datos = f_leer_archivo("archivo_tradeview_1.csv")
    """
    
    # Se forma una nueva columna inicializada en $5,000 donde se le suma/resta el profit acumulado en cada renglón
    datos['capital_acm'] = 5000 + datos.profit_acm 
    return datos.copy()

#%% 
# Cálculo del profit diario
    
def f_profit_diario(datos):
     """
     Parameters
     ----------
     datos : pandas.DataFrame : dataframe de fechas históricas solo usando columnas timestamp y profit
  
     Returns
     -------
     datos : pandas.DataFrame : dataframe con las columnas timestamp, profit diario y el acumulado
  
     Debugging
     ---------
     datos = f_leer_archivo("archivo_tradeview_1.xlsx")

     """
     pass
  

#%%
    
# Terminar el profit acumulado diario antes de terminar stats mad
    
def f_stats_mad(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : dataframe con transacciones ejecutadas después de tiempos y pips
    
    Returns
    -------
    datos : pandas.DataFrame : dataframe con rendimientos logarítmicos. Tomando en cuenta que se inicializa con una cuenta de $5,000

    Debugging
    ---------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    
    """
    rend_log = np.log(datos.capital_acm[1:].values/datos.capital_acm[:-1].values)
    # benchmark = 
    # rend_log_bench = np.log(datos_benchmark...)
    # tracking_error = rend_log - rend_log_bench
    
    # https://towardsdatascience.com/python-for-finance-stock-portfolio-analyses-6da4c3e61054
    # https://www.investopedia.com/terms/i/informationratio.asp    
    rf = 0.08
    
    #%%
    #TIP DEL PROFE
    #df_data.groupby('fechas_dias')['profit'].sum()
    #%%
    # Cambiar a semanal los datos
    # Agregar un benchmark SP500
    MAD = pd.DataFrame({
        'sharpe': (rend_log.mean()*30 - rf) / rend_log.std()*(30**0.5),
        'sortino_b': (rend_log.mean()*30 - rf) / rend_log[rend_log >= 0].std()*(30**0.5),
        'sortino_s': (rend_log.mean()*30 - rf) / rend_log[rend_log < 0].std()*(30**0.5),
        # Que de donde se inicia, no hayan valores mayores al punto de inicio y sea solo tendencia bajista
        # 'drawdown_cap': 
        # Que de donde se inicia, no hayan valores menores al punto de inicio y que sea solo tendencia alcista
        # 'drawup_cap': 
        #'drawdown_pips': datos.pips_acm...,
        #'drawup_pips': datos.pips_acm.. #,
        # 'information_ratio': (rend_log.mean()*7 - rend_log_bench.mean()*7) / tracking_error.std()*7**0.5
        }, index = ['Valor']).transpose()

    return MAD

#%% Parte 4: Sesgos cognitivos del trader

# def f_sesgos_cognitivos():
#     """
#     Parameters
#     ----------
    
#     Returns
#     -------
    
#     Debugging
#     ---------
    
#     """
    
#     pass
    
# Disposission effect














 