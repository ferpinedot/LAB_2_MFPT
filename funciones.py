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
import pandas_datareader.data as web
import datetime 


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
    df_1_ranking : pd.DataFrame : dataframe con un ranking entre el 0 y el 1 en donde se califica con cuales divisas se obtuvieron operaciones precisas realizadas
        
    Debugging
    ---------
    datos = f_leer_archivo("archivo_tradeview_1.xlsx")
    """
    
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
                                'r_proporcion': [len(datos[datos['profit'] >= 0]) / len(datos[datos['profit'] < 0]), 'Ganadoras Totales/Perdedoras Totales'],
                                'r_efectividad_b': [len(datos[(datos['type'] == 'buy') & (datos['profit'] >= 0)]) / len(datos['order']), 'Operaciones ganadoras de compra/Operaciones Totales'],
                                'r_efectividad_s': [len(datos[(datos['type'] == 'sell') & (datos['profit'] >= 0)]) / len(datos['order']), 'Operaciones ganadoras de venta/Operaciones Totales'],
                                }, index = ['Valor', 'Descripción']).transpose()
    
    tb1 = pd.DataFrame({i: len(datos[datos.profit >0][datos.symbol == i])/len(datos[datos.symbol == i])
                        for i in datos.symbol.unique()}, index = ['rank']).transpose()
    
    convert_dict = {'Valor': float} 
    df_1_tabla = df_1_tabla.astype(convert_dict) 
    
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
     # cantidad de operaciones cerradas ese dia
     datos['ops'] = [i.date() for i in datos.closetime] 
     diario = pd.date_range(datos.ops.min(),datos.ops.max()).date
     # convertir a dataframe las fechas diarias
     fechas = pd.DataFrame({'timestamp' : diario})
     
     groups = datos.groupby('ops')
     profit = groups['profit'].sum()
     # convertir los profits diarios a dataframe
     profit_diario = pd.DataFrame({'profit_d' : [profit[i] if i in profit.index else 0 for i in diario]})
     profit_acm = np.cumsum(profit_diario) + 5000
     # juntar en un solo dataframe los dos dataframes anteriores fechas y profits diarios
     f_p1 =pd.merge(fechas, profit_diario, left_index = True, right_index = True)
     # juntar el dataframe anterior de los dos df con los profits acumulados
     df_profit_diario1 = pd.merge(f_p1, profit_acm, left_index = True, right_index = True)
     # renombrar las columnas del nuevo dataframe
     df_profit_diario = df_profit_diario1.rename(columns = {"profit_d_x" : "profit_d", "profit_d_y" : "profit_acm_d"})
     
     return df_profit_diario
 
#%%
     
def adj_close(tickers, start_date=None, end_date=None):
    """
    Parameters
    ----------
    tickers : Type 
    start_date : datetime
    end_date : datetime

    Returns
    -------
    close : Type

    """
    # Descargar dataframe con datos de precio de cierre ajustado
    close = web.DataReader(name = tickers, data_source = 'yahoo', start = start_date, end = end_date)
    close = close['Adj Close']
    close.sort_index(inplace=True)
    return close
     
#%%
     
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
    rf = 0.08/300
    mar = 0.3/300
    # rb = 0.0832/300
    
    profit_d = f_profit_diario(datos)
     
    # DD y DU
    where_row = profit_d.loc[profit_d['profit_acm_d'] == profit_d.profit_acm_d.min()]
    where_position = where_row.index.tolist()
    
    # Drawdown
    prev_where = profit_d.loc[0:where_position[0]]
    max_prev_where = prev_where.max()
    min_prev_where = prev_where.min()
    dd = max_prev_where['profit_acm_d'] - min_prev_where['profit_acm_d']
    drawdown = list([min_prev_where['timestamp'], max_prev_where['timestamp'], dd])
 
    # Drawup
    foll_where = profit_d.loc[where_position[0]:]
    max_foll_where = foll_where.max()
    min_foll_where = foll_where.min()
    du = max_foll_where['profit_acm_d'] - min_foll_where['profit_acm_d']
    drawup = list([min_foll_where['timestamp'], max_foll_where['timestamp'], du])
     
    # Information Ratio
    # ir_num = rend_log.mean() - rb
    # y = slice(0, 10, 1)
    start = datos['closetime'].min() # [y]
    end = datos['closetime'].max() # [y]
    close = adj_close(tickers='^GSPC', start_date=start, end_date=end)
    rb = np.log(close / close.shift(1)).iloc[1:]
    rend_tot = [str(i)[1:] for i in rend_log]
    precios = [float(i) for i in rend_tot]
    for i in range(len(precios)):
        benchmark = precios[i] - rb
    # df_mad.loc['information_r', ['valor', 'descripcion']] = [(rend_log.mean()-rb.mean())/benchmark.std(), 'Information Ratio']
     
    
    # Métricas
    metrica = pd.DataFrame({'métricas': ['sharpe', 'sortino_b', 'sortino_s', 'drawdown_cap_b', 'drawdown_cap_s', 'information_r']})
    valor = pd.DataFrame({'valor' : [((rend_log.mean() - rf)/ rend_log.std()), 
                                     ((rend_log.mean() - mar) / rend_log[rend_log >= 0].std()), #rend compra.mean() - mar / 
                                     ((rend_log.mean() - mar) / rend_log[rend_log < 0].std()),
                                     (drawdown),
                                     (drawup),
                                     ((rend_log.mean()-rb.mean())/benchmark.mean())
                                     ]})
    
    df_mad1 = pd.merge(metrica, valor, left_index = True, right_index = True)
    descripcion = pd.DataFrame({'descripción': ['Sharpe Ratio', 'Sortino Ratio para Posiciones de Compra', 'Sortino Ratio para Posiciones de Venta', 'DrawDown de Capital', 'DrawUp de Capital', 'Information Ratio']})
    df_MAD = pd.merge(df_mad1, descripcion, left_index = True, right_index= True)
    # convert_dict = {'valor': float} 
    # df_MAD = df_MAD.astype(convert_dict) 
    
    return df_MAD
    
#%% Parte 4: Sesgos cognitivos del trader
#%%

def f_sesgos_cognitivo(datos):
    """
    Parameters
    ---------
    datos : pandas.DataFrame : informacion de las operaciones 

    Returns
    ---------
    

    Debuggin
    ---------
    datos = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
    
    pass