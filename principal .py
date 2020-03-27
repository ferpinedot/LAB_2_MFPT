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

import funciones as fn

# Leer el archivo
#1
#archivo = "archivos/archivo_tradeview_1.csv"
# 2
# archivo = "archivos/archivo_tradeview_1.xlsx"
# datos = fn.f_leer_archivo(archivo)
#3
datos = fn.f_leer_archivo(param_archivo='archivos/archivo_tradeview_1.xlsx', sheet_name= 0)

# Tiempo de la operación
datos = fn.f_columnas_tiempos(datos)

# Número de pips
datos = fn.f_columnas_pips(datos)

# Capital acumulado ($)
datos = fn.f_capital_acm(datos)

# Estadísticas básicas
estadisticas = fn.f_basic_stats(datos)

# Estadísticas de desempeño de movimientos
profit_d = fn.f_profit_diario(datos)
desempeno = fn.f_stats_mad(datos)

## Behavioral Finance, sesgos cognitivos
# sesgos = fn.f_sesgos_cognitivos(datos)

# print(datos)
# print(estadisticas['df_1_tabla'])
# print(estadisticas['df_1_ranking'])
# print(desempeno)
#print(sesgos)