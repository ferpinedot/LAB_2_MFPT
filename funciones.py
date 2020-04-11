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
import datos as dt
import datetime 
import math
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

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
                'chfjpy': 100, 'audjpy': 100,
                'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                'audusd': 10000, 'nzdusd': 10000, 'usdchf': 10000, 'eurgbp': 10000,
                'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000, 'gbpnzd': 10000,
                'gbpchf': 10000, 'gbpaud': 10000, 'audnzd': 10000, 'nzdcad': 10000,
                'nzdjpy': 10000, 'audchf': 10000, 'cadchf': 10000, 'gbpcad': 10000, 
                'audcad': 10000, 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pip_inst[inst]

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
     
     # Agregar normalize a closetime
     diario = pd.date_range(datos.closetime.min(), datos.closetime.max()).normalize()
     
     # convertir a dataframe las fechas diarias
     fechas = pd.DataFrame({'timestamp' : diario})
     
     # Agregar normalize a groupby
     groups = datos.groupby(pd.DatetimeIndex(datos['closetime']).normalize())
     
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
    profit_d = f_profit_diario(datos)
    
    # Sharpe ratio
    rend_log = np.log(profit_d.profit_acm_d[1:].values/profit_d.profit_acm_d[:-1].values)
    rf = 0.08/300
    mar = 0.3/300
    
        
    # Sortino compra
    # Numerador
    s_buy = (f_profit_diario(datos[datos['type'] == 'buy']))
    rend_log_b = np.log(s_buy.profit_acm_d[1:].values / s_buy.profit_acm_d[:-1].values)
    # Denominador
    tdd_sb = rend_log_b - mar
    tdd_sb[tdd_sb > 0] = 0
    # Final
    sortino_b = (rend_log_b.mean() - mar) / (((tdd_sb*2).mean())*0.5)
    

    # Sortino venta
    # Numerador
    s_sell = (f_profit_diario(datos[datos['type'] == 'sell']))
    rend_log_s = np.log(s_sell.profit_acm_d[1:].values / s_sell.profit_acm_d[:-1].values)
    # Denominador
    tdd_ss = rend_log_s - mar
    tdd_ss[tdd_ss > 0] = 0
    # Final
    sortino_s = (rend_log_s.mean() - mar) / ((tdd_ss*2).mean())*0.5
    
    
    
    # DD y DU
    where_row = profit_d.loc[profit_d['profit_acm_d'] == profit_d.profit_acm_d.min()]
    where_position = where_row.index.tolist()
    
    # Drawdown
    prev_where = profit_d.loc[0:where_position[0]]
    where_max_prev = profit_d.loc[profit_d['profit_acm_d'] == prev_where.profit_acm_d.max()]
    where_min_prev = profit_d.loc[profit_d['profit_acm_d'] == prev_where.profit_acm_d.min()]
    max_dd = where_max_prev.iloc[0]['profit_acm_d']
    min_dd = where_min_prev.iloc[0]['profit_acm_d']
    dd = max_dd - min_dd
    fecha_i_dd = where_max_prev.iloc[0]['timestamp']
    fecha_f_dd = where_min_prev.iloc[0]['timestamp']
    drawdown =  "{}, {}, ${:.2f}" .format(fecha_i_dd, fecha_f_dd, dd)
     
    # Drawup
    foll_where = profit_d.loc[where_position[0]:]
    where_max_foll = profit_d.loc[profit_d['profit_acm_d'] == foll_where.profit_acm_d.max()]
    where_min_foll = profit_d.loc[profit_d['profit_acm_d'] == foll_where.profit_acm_d.min()]
    max_du = where_max_foll.iloc[0]['profit_acm_d']
    min_du = where_min_foll.iloc[0]['profit_acm_d']
    du = max_du - min_du
    fecha_f_du = where_max_foll.iloc[0]['timestamp']
    fecha_i_du = where_min_foll.iloc[0]['timestamp']
    drawup =  "{}, {}, ${:.2f}" .format(fecha_i_du, fecha_f_du, du)        

    
    # Information Ratio
    benchmark_original = pd.DataFrame(web.YahooDailyReader('^GSPC', profit_d['timestamp'].min(), profit_d['timestamp'].max(), interval='d').read()['Adj Close'])
    # Ajustar fechas como columna en el dataframe
    benchmark = benchmark_original.reset_index()
    # Agregar columna de los rendimientos logarítmicos de los precios de Cierre Ajustado del SP500
    benchmark['rend_log'] = pd.DataFrame(np.log(benchmark['Adj Close'][1:].values / benchmark['Adj Close'][:-1].values))
    # Juntar el dataframe de profits con el benchmark en uno solo
    bench_merge = profit_d.merge(benchmark,  left_on = 'timestamp', right_on = 'Date')
    # Recorrer los valores de los rendimientos logarítmicos una posición abajo y llenar con 0
    bench_merge['rend_log'] = bench_merge['rend_log'].shift(1, fill_value = 0)
    
    # Cálculo de rendimientos logarítmicos de los profit_acm_d
    rend_log_profit = pd.DataFrame(np.log(bench_merge.profit_acm_d[1:].values/bench_merge.profit_acm_d[:-1].values))
    # rend_log_profit = rend_log_profit.shift(1, fill_value = 0)
    
    # Agregar la columna de rendimientos de profit_acm_d 
    bench_merge.insert(3, column = 'rend_log_profit', value = rend_log_profit)
    # Recorrer una fila hacia abajo los rendimientos en el dataframe
    bench_merge['rend_log_profit'] = bench_merge['rend_log_profit'].shift(1, fill_value = 0)
    
    # Numerador Information Ratio
    # Promedio de rendimientos del profit_acm_d
    profit_prom = bench_merge['rend_log_profit'].mean()
    # Promedio de rendimientos del SP500
    bench_prom = bench_merge['rend_log'].mean()
    # Numerador del information ratio = diferencia de los dos anteriores
    num_ir = profit_prom - bench_prom
    
    # Denominador Information Ratio
    # Diferencia por rows de los rendimientos del profit_acm_d y del SP500
    dif_denom = bench_merge['rend_log_profit'] - bench_merge['rend_log']
    # Desviación estándar de la diferencia
    denom_ir = dif_denom.std()
    
    # Cálculo del ratio
    info_ratio = num_ir/denom_ir
    
    
    # Métricas
    metrica = pd.DataFrame({'métricas': ['sharpe', 'sortino_b', 'sortino_s', 'drawdown_cap_b', 'drawdown_cap_s', 'information_r']})
    valor = pd.DataFrame({'valor' : [((rend_log.mean() - rf)/ rend_log.std()), 
                                     (sortino_b),
                                     (sortino_s),
                                     (drawdown),
                                     (drawup),
                                     (info_ratio)
                                     ]})
    
    df_mad1 = pd.merge(metrica, valor, left_index = True, right_index = True)
    descripcion = pd.DataFrame({'descripción': ['Sharpe Ratio', 'Sortino Ratio para Posiciones de Compra', 'Sortino Ratio para Posiciones de Venta', 'DrawDown de Capital', 'DrawUp de Capital', 'Information Ratio']})
    df_MAD = pd.merge(df_mad1, descripcion, left_index = True, right_index= True)
    # convert_dict = {'valor': float} 
    # df_MAD = df_MAD.astype(convert_dict) 
    
    return df_MAD
    
#%% Parte 4: Sesgos cognitivos del trader
#%%

def f_prices(param_ins, date):
    """
    Parameters
    ----------
    param_ins : str : instrumento del cual se requiere obtener el precio
    date : date : fecha en la que se requiere el precio del instrumento

    Returns
    -------
    float : precio del instrumento en la fecha que se pidió en opening
    
    Debuggin
    --------
    """
    # Descargar los precios de apertura:
    
    # Inicializar API de OANDA
    api_oa = API(environment = "practice", access_token = dt.OA_Ak)
    # Volver la fecha a str
    fecha = date.strftime('%Y-%m-%dT%H:%M:%S')
    # Definir los parámetros 
    parameters = {"count": 1, "dailyAlignment": 16, "from": fecha, "granularity": 'M1', "price": "M"}
    # Definir el instrumento y con los parámetros con los que se descargarán de OANDA
    instrumento = instruments.InstrumentsCandles(instrument = param_ins, params = parameters)
    # Descargarlo de OANDA
    response = api_oa.request(instrumento)
    # En fomato candles se encuentran los precios
    prices = response.get("candles")
    # Dentro de candles entrar al diccionario 0 y posteriormente al 'mid' donde están el precio cierre 'c', high 'h', low 'l', y open 'o'
    return float(prices[0]['mid']['o'])


def f_instrument(ins):
    """
    Parameters
    ----------
    ins : str : instrumento del precio que se necesite

    Returns
    -------
    str : instrumento con un formato en mayúsculas y con _ cada 3 letras
    
    Debuggin
    --------
    instrument = 'usdmxn'
    
    """
    # Cambiar automáticamente el nombre de los instrumentos en minúscula a mayúscula y
    # cambiando al formato para que OANDA pueda leer qué instrumentos
    return ins.upper()[:3] + '_' + ins.upper()[3:]


def f_be_de(datos):
    """
    Parameters
    ----------
    datos : pd.DataFrame : Archivo original de las operaciones realizadas
    Returns
    -------
    pd.DataFrame : Archivo de operaciones
    
    Debuggin
    --------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    """
    
    # Crear una nueva columna en el dataframe de datos con un ratio del profit por operación entre el capital acumulado
    # Únicamente el primer valor del profit se divide entre $5,000 por ser los $5,000 todo el capital hasta el momento
    datos['profit/cap (%)'] = [(datos['profit'][i]/5000)*100 if i == 0 else (datos['profit'][i]/datos['capital_acm'][i-1])*100 for i in range(len(datos['profit']))]
      
    # Dataframe con operaciones perdedoras
    df_perd= datos[datos['profit'] < 0]
    df_perd.reset_index(inplace = True, drop = True)

    # Dataframe con operaciones ganadoras
    df_gand = datos[datos['profit'] > 0]
    df_gand.reset_index(inplace = True, drop = True)
    
    # Con las operaciones ya ganadas, buscar las operaciones que pertenecen a los cuatro escenarios en los que habrían posibles ocurrencias
    posibles_operaciones = [[datos.iloc[i,:] for i in range(len(datos)) 
                             # Que la operación haya abierto antes que la ganadora y cerrado después de la ganadora
                             if datos['opentime'][i] < df_gand['opentime'][k]  and                                  
                             datos['closetime'][i] > df_gand['closetime'][k] or
                             # Que la operación ganadora haya iniciado antes, y haya cerrado antes que la operación abierta
                             df_gand['closetime'][k] > datos['opentime'][i] > df_gand['opentime'][k] and
                             # Y que la operación abierta haya cerrado después del momento de cierre de la operación ganadora
                             datos['closetime'][i] > df_gand['closetime'][k]]
                             for k in range(len(df_gand))]
    
    # Colocar todas las posibles operaciones en formato dataframe en donde la primera, es la operación ancla, y cada dataframe en una lista
    pos_ops = [pd.concat([df_gand.iloc[i, :], pd.concat(posibles_operaciones[i], axis = 1)], 
                         axis = 1, sort=False, ignore_index = True).T for i in range(len(posibles_operaciones)) if posibles_operaciones[i] != []]
    
    # Se descargan los precios de cierre en una lista de acuerdo a la operación ancla (ganadora)
    prices = [[f_prices(f_instrument(pos_ops[k]['symbol'][i+1]), pos_ops[k]['closetime'][0])
               for i in range(len(pos_ops[k]) - 1)] for k in range(len(pos_ops))]
    
    # Lista de todas las posibles ocurrencias en formato dataframe
    prices_pos_ops = [pd.concat([pos_ops[i], pd.concat([pd.DataFrame([0], columns=['prices_on_close']), pd.DataFrame(prices[i], columns=['prices_on_close'])],
                                                       sort=False, ignore_index = True)], axis = 1, sort=False) for i in range(len(pos_ops))]
    
    # Llenar lista con Diccionarios
    ocurrencias = []
    k = 0
    # Se agrega la pérdida flotante
    for i in range(len(prices_pos_ops)): 
        prices_pos_ops[i]['perdida_flotante'] = (prices_pos_ops[i]['prices_on_close'] - prices_pos_ops[i]['openprice'])*(prices_pos_ops[i]['profit'] / (prices_pos_ops[i]['closeprice'] - prices_pos_ops[i]['openprice'])) 
    # Se guarda la pérdida flotante y se toma la máxima          
    for j in range(len(prices)):
        profits, indexes = [],  []
        for i in range(len(prices[j])):
            if prices[j][i] < pos_ops[j]['openprice'][
                    i+1] and pos_ops[j]['type'][i+1] == 'buy' or prices[
                            j][i] > pos_ops[j]['openprice'][
                                    i+1] and pos_ops[j]['type'][i+1] == 'sell':   
                profits.append((prices_pos_ops [j]['perdida_flotante'][i+1]))
                indexes.append(i+1)
        
        # Se hace el cálculo de las ocurrencias 
        if profits != []:
            indx = profits.index(min(profits))
            k +=1
            new_profits = round((prices_pos_ops[j]['prices_on_close'][indexes[indx]] - pos_ops[j]['openprice'][indexes[indx]]) * ((pos_ops[j]['profit'][indexes[indx]]) / (pos_ops[j]['closeprice'][indexes[indx]] - pos_ops[j]['openprice'][indexes[indx]])), 3)                            
            ocurrencias.append({'ocurrencia %d'%k:
                                    {'timestamp': pos_ops[j]['closetime'][0],
                                     'operaciones':
                                             {'ganadora':  
                                                    {'instrumento': pos_ops[j]['symbol'][0],
                                                     'sentido': pos_ops[j]['type'][0],
                                                     'volumen': pos_ops[j]['size'][0],
                                                     'capital_gand': pos_ops[j]['profit'][0],
                                                     'capital_acm': pos_ops[j]['capital_acm'][0]},  
                                               'perdedora':
                                                    {'instrumento': pos_ops[j]['symbol'][indexes[indx]],
                                                     'sentido': pos_ops[j]['type'][indexes[indx]],
                                                     'volumen': pos_ops[j]['size'][indexes[indx]],
                                                     'profit': pos_ops[j]['profit'][indexes[indx]],
                                                     'capital_perd': new_profits}},
                                      'ratio_cp_capital_acm': round(abs(new_profits/pos_ops[j]['capital_acm'][0])*100, 3),                                            
                                      'ratio_cg_capital_acm': round(abs(pos_ops[j]['profit'][0] / pos_ops[j]['capital_acm'][0])*100, 3),
                                      'ratio_cp_cg': round(abs(new_profits/pos_ops[j]['profit'][0]), 3)}})
           
    data = pd.concat([pd.DataFrame([ocurrencias[i-1]['ocurrencia %d'%i]['ratio_cp_capital_acm'],
                                    ocurrencias[i-1]['ocurrencia %d'%i]['ratio_cg_capital_acm'],
                                    ocurrencias[i-1]['ocurrencia %d'%i]['ratio_cp_cg'],
                                    ocurrencias[i-1]['ocurrencia %d'%i]['operaciones']['ganadora']['capital_acm']])
                      for i in range(1, len(ocurrencias)+1)], axis=1, ignore_index = True).transpose()

    first_last = pd.concat([data.iloc[0,:], data.iloc[len(data)-1, :]], axis=1, ignore_index=True).transpose()
    
    # DataFrame de resultados de ocurrencias 
    names = pd.DataFrame(['ocurrencias', 'status_quo', 'aversión_pérdida', 'sensibilidad_decreciente'])
    results = pd.DataFrame([(len(data)), 
                            (len([1 for i in range(len(data)) if data.iloc[i,0] < data.iloc[i,1]]) / len(data)),
                            (len([1 for i in range(len(data)) if data.iloc[i,2] > 1.5]) / len(data)),
                            ('Sí' if first_last.iloc[0,3] < first_last.iloc[1,3] and 
                             first_last.iloc[1,2] > 1.5 and
                             (first_last.iloc[0,0] < first_last.iloc[1,0] or 
                             first_last.iloc[0,1] < first_last.iloc[1,1]) else 'No')]) 
    # Mergear los dataframes con nombres y resultados     
    f_results = pd.merge(names, results, left_index = True, right_index = True)
    f_results_c = f_results.rename(columns = {"0_x": "mediciones", "0_y": "resultados"})
    
    # Entrega final de diccionario con la lista de ocurrencias y el dataframe de resultados del análisis de ocurrencias 
    return {'ocurrencias': ocurrencias, 'resultados': f_results_c}