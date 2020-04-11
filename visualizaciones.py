# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:37:44 2020

@author: User
"""

import matplotlib.pyplot as plt
import funciones as fn
import plotly.graph_objects as go
import plotly.offline as py
py.offline.init_notebook_mode(connected = False)
#from plotly.offline import iplot
import pandas as pd
 

# datos = fn.f_leer_archivo(param_archivo='archivos/archivo_tradeview_1.xlsx', sheet_name= 0)
datos = fn.f_leer_archivo(param_archivo='archivos/archivo_pap_.xlsx', sheet_name= 0)
# datos = fn.f_leer_archivo(param_archivo='archivos/archivo_oanda.xlsx', sheet_name= 0)

datos = fn.f_columnas_tiempos(datos)

# Número de pips
datos = fn.f_columnas_pips(datos)

# Capital acumulado ($)
datos = fn.f_capital_acm(datos)

profit_d = fn.f_profit_diario(datos)

def profitd(datos):
    """
    Parameters
    ----------
    datos : pd.DataFrame : Datos de siempre 

    Returns
    -------
    graph : gráfica de matplotlib color magenta para mostrar el profit acumulado

    """ 
    profit_d.plot(x= 'timestamp' , y= 'profit_acm_d', kind = 'line', color = 'm')
    plt.xticks(rotation=45)
    plt.xlabel('tiempo')
    plt.ylabel('profit ($)')
    plt.show()
    

def profit_acum(profit_d):
    """
    Parameters
    ----------
    profit_d : función : Función utilizada para el dataframe con el pd.DataFrame(datos)

    Returns
    -------
    graph: gráfica de barras con plotly mostrando el profit acumulado

    """
    profit_d = fn.f_profit_diario(datos)
    fig = go.Figure(data = [go.Bar(x = profit_d['timestamp'], y = profit_d['profit_acm_d'])], layout_title_text = "A fig.show()")
    # fig.show()
    py.iplot(fig)
    

# def profit_acum_line(profit_d):
#     """
#     Parameters
#     ----------
#     profit_d : función : Función utilizada para el dataframe con el pd.DataFrame(datos)

#     Returns
#     -------
#     graph : gráfica de línea con plotly mostrando el profit acumulado

#     """
#     profit_d = fn.f_profit_diario(datos)
#     profs = go.Figure(data = [go.Scatter(x= profit_d['timestamp'], y = profit_d['profit_acm_d'], mode = 'lines', marker = dict(color = 'Black'))])
#     profs.update_layout(title = "Profit acumulado al día", xaxis_title = "Tiempo (fechas)", yaxis_title = "Profit ($)")
#     #profs.show()
#     py.iplot(profs)


# Gráfica de ranking
def ranking(estadisticas):
    """
    Parameters
    ----------
    estadisticas : función : Función utilizada para calcular el ranking de asertividad de divisas

    Returns
    -------
    graph : gráfica de pastel con plotly mostrando el porcentaje que representa la asertividad del total de pares usados

    """
    estadisticas = fn.f_basic_stats(datos)
    df_ranking = pd.DataFrame(estadisticas['df_1_ranking'])
    df_1_ranking = df_ranking.reset_index()
    df_ranking = df_1_ranking.rename(columns = {"index": "pares", "rank": "rank"})
    
    pie_rank = go.Figure()
    labels = df_ranking['pares']
    values = df_ranking['rank']
    pie_rank = go.Figure(data = [go.Pie(labels=labels, values=values, pull=[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])])
    pie_rank.update_layout(title = "Ranking de asertividad de pares", font = dict(size = 16))
    #pie_rank.show()
    py.iplot(pie_rank)
    

profit_d = fn.f_profit_diario(datos)

# Gráfica drawdown y drawup
def profit_dd_du_line(profit_d):
    """
    Parameters
    ----------
    profit_d : función : Función utilizada para el dataframe con el pd.DataFrame(datos)

    Returns
    -------
    graph : gráfica de línea con plotly mostrando el profit acumulado

    """
    profit_d = fn.f_profit_diario(datos)

    profs = go.Figure()
    profs.add_trace(go.Scatter(x = profit_d.timestamp, y = [None, None, None, None, 4529.32, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 4989.32, None, None, None, None, None, None, None, None, None, None, None, None] , name = 'drawup', connectgaps=True, mode = 'lines', line={'dash': 'dash', 'color': 'green'}))
    profs.add_trace(go.Scatter(x = profit_d.timestamp, y = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 4989.32, None, None, None, None, None, None, None, 4117.03, None, None, None, None] , name = 'drawdown', connectgaps=True, mode = 'lines', line={'dash': 'dash', 'color': 'red'}))
    profs.add_trace(go.Scatter(x= profit_d.timestamp, y = profit_d.profit_acm_d, name = 'profit acumulado', mode = 'lines', marker = dict(color = 'Black')))
    
    profs.update_layout(title = "Profit acumulado al día", xaxis_title = "Tiempo (fechas)", yaxis_title = "Profit ($)")
    
    #profs.show()
    py.iplot(profs)



# def sesgos_graph(sesgos):
#     """
#     Parameters
#     ----------
#     sesgos : función : Función utilizada para calcular los sesgos cognitivos 

#     Returns
#     -------
#     graph : gráfica de barras representando valores porcentuales del status-quo y aversión al riesgo

#     """
    
#     sesgos = fn.f_sesgos_cognitivos(datos)
#     df_resultados = pd.DataFrame(sesgos['resultados'])
#     df_results = df_resultados.drop([0, 3])
#     sesgs_bar = go.Figure(data = [go.Bar(x = df_results['mediciones'], y = df_results['resultados'])])
#     sesgs_bar.update_layout(title = "Disposition Effect", xaxis_title = "Mediciones", yaxis_title = "Resultados (%)")    
#     sesgs_bar.show()
 
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    