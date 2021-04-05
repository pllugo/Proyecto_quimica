#!/usr/bin/env python
'''
Impactos Ambientales
---------------------------
Autor: Pedro Luis Lugo Garcia
Version: 1.0
 
Descripcion:
Programa creado para buscar los parámetros para calcular
el valor estimado de POCP de un COV en la atmosfera.
'''

__author__ = "Pedro Luis Lugo Garcia"
__email__ = "pedro.lugo@unc.edu.ar"
__version__ = "1.0"

import parametros_ozono
import math
import parametros_acidificacion
import compuestos


def potencial_ozono(condicion_a, condicion_f, numero_enlaces, peso_molecular, numero_carbonos, koh_compuesto, ko3_compuesto, koh_producto, rendimiento_molar, condicion_p, condicion_ro3, condicion_q, region):
     #condicion_f, koh_producto, rendimiento_molar, 
    tupla_a = parametros_ozono.busqueda_parametro(condicion_a, region)
    lista_a = sorted(set().union(*tupla_a))
    if condicion_f != 0 and koh_producto != 0 and koh_producto <2E-12:
        valor_delta = lista_a[1] * (1 - (1E12 * koh_producto / 2)) * 1E12 * koh_producto ** lista_a[0]
        valor_f = ((numero_enlaces - ( rendimiento_molar * numero_enlaces))/ numero_enlaces) ** valor_delta
    else:
        valor_f = 1
    if condicion_p !=0:
        valor_p = sorted(set().union(*parametros_ozono.busqueda_parametro(condicion_p, region)))[0]
    else:
        valor_p = 0
    if condicion_q !=0:
        valor_q = sorted(set().union(*parametros_ozono.busqueda_parametro(condicion_q, region)))[0]
    else:
        valor_q = 0
    if condicion_ro3 !=0:
        lista_ro3 = sorted(set().union(*parametros_ozono.busqueda_parametro(condicion_ro3, region)))
        valor_mu = ((ko3_compuesto/ 1.55E-18) * (koh_compuesto / 7.80E-12)) ** lista_ro3[0]
        valor_ro3 = lista_ro3[1] ** valor_mu
    #AHORA A CALCULAR POCP
    valor_b = sorted(set().union(*parametros_ozono.busqueda_parametro("B", region)))[0]
    valor_alfa = sorted(set().union(*parametros_ozono.busqueda_parametro("alfa", region)))[0]
    valor_c = sorted(set().union(*parametros_ozono.busqueda_parametro("C", region)))[0]
    valor_beta = sorted(set().union(*parametros_ozono.busqueda_parametro("beta", region)))[0]
    valor_gamma = (numero_enlaces / 6) * (28.05 / peso_molecular)
    gamma_r = (koh_compuesto / 7.80E-12) * (6 / numero_enlaces)
    valor_r = 1 - (1 / (valor_b * gamma_r + 1))
    valor_s = (1 - valor_alfa) * math.e ** (-valor_c * numero_carbonos ** valor_beta) + valor_alfa
    valor_pocp = round((lista_a[2] * valor_gamma * valor_r * valor_s * valor_f) + valor_p + valor_ro3 - valor_q, 2)
    print(valor_pocp)
    return valor_pocp

def tiempo_residencia(constante_cinetica, tipo_radical):#Función para calcular el tiempo de residencia
    if tipo_radical == "OH":                           #atmosferico de un COV
        tiempo = round(1 / (constante_cinetica * 1E6), 2)
    else:
        if tipo_radical == "Cl":
            tiempo = round(1 / (constante_cinetica * 1E4), 2)
        else:
            if tipo_radical == "NO3":
                tiempo = round(1 / (constante_cinetica * 5E8), 2)
            else:
                print("O3")
                tiempo = round(1 / (constante_cinetica * 7E11), 2)
    return tiempo

def potencial_acidificacion(peso_molecular, numero_cloro, numero_fluor, numero_nitrogeno, numero_azufre):
    potencial_ap = round((64.066 / peso_molecular) * (numero_cloro + numero_fluor + numero_nitrogeno + 2 * numero_azufre) / 2, 2)
    lista_acida = parametros_acidificacion.busqueda_compuestos_potenciales(potencial_ap)
    return potencial_ap, lista_acida


