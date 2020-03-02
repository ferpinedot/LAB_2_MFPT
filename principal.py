
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Fernanda Pinedo
# -- repositorio: https://github.com/ferpinedot/LAB_2_MFPT
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

#datos de entrada
datos = fn.f_leer_archivo(param_archivo='archivo_mt4.xlsx')

#
df_data = fn.f_columnas_tiempos(df_data)

#param_ins='usdjpy'
#fn.f_pip_size(param_ins)