#!/usr/bin/env python
'''
API Química Atmosférica
---------------------------
Autor: Pedro Luis Lugo Garcia
Version: 1.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
los experimentos que se realizan en LUCQA.
'''

__author__ = "Pedro Luis Lugo Garcia"
__email__ = "pedro.lugo@unc.edu.ar"
__version__ = "1.0"

import numpy as np
import csv
import impactos
import sqlite3
import compuestos
import traceback
import io
import sys
import os
import base64
import json
from datetime import datetime, timedelta
import pandas as pd
import math

from flask import Flask, request, jsonify, render_template, Response, redirect , url_for, session
from flask_sqlalchemy import SQLAlchemy
import matplotlib
matplotlib.use('Agg')   # For multi thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


app = Flask(__name__)



@app.route('/')
def indices():
    return render_template ('indices.html')


#Ruta para ingresar los datos de los COVs a la base de datos
@app.route('/datos', methods=['GET', 'POST'])
def datos_cov():
    if request.method == "POST":
        peso_molecular_cov = float(request.form['peso_molecular'])
        densidad_cov = float(request.form['densidad'])
        formula = request.form['formula']
        nombre_cov = request.form['nombre']
        abreviatura_cov = request.form['abreviatura']
        sustituyentes_cov = request.form.get('sustituyente')
        enlaces_cov = request.form.get('enlace')
        #Conectar a la base de datos
        compuestos.insert_compuestos(formula, nombre_cov, abreviatura_cov, densidad_cov, peso_molecular_cov, sustituyentes_cov, enlaces_cov, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        return render_template('acidificacion.html', peso_molecular_cov=peso_molecular_cov, abreviatura_cov=abreviatura_cov)
    return render_template('datoscovs.html')

#Ruta para mostrar todos los resultados en un dashboard
@app.route('/resultados')
def estadistica():
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()
    lista_cov = []
    for row in c.execute('SELECT nombre, t_oh, ap_cov, pocp_cov, gwp_20, gwp_100, gwp_500 FROM compuestos'):
        lista_cov.append(row)
    resultado = []
    covs = []
    ap = []
    pocp = []
    t_oh =[]
    gwp_cov_20 = []
    gwp_cov_100 = []
    gwp_cov_500 = []
    radical = "OH"
    for i in range(len(lista_cov)):
        resultado = list(lista_cov[i])
        print(resultado)
        covs.append(resultado[0])
        t_oh.append(resultado[1])
        ap.append(resultado[2])
        pocp.append(resultado[3])
        gwp_cov_20.append(resultado[4])
        gwp_cov_100.append(resultado[5])
        gwp_cov_500.append(resultado[6])
    #Tomo los datos AP, POCP, tiempo y GWP     
    ap_compuesto = ap[len(ap)-1]
    tiempo = t_oh[len(t_oh)-1]
    pocp_compuesto = pocp[len(pocp)-1]
    gwp_covs_20 = round(gwp_cov_20[len(gwp_cov_20)-1], 3)
    gwp_covs_100 = round(gwp_cov_100[len(gwp_cov_100)-1], 3)
    gwp_covs_500 = round(gwp_cov_500[len(gwp_cov_500)-1], 3)
    conn.close()
    return render_template('resultados.html', covs=covs, ap=ap, pocp=pocp, ap_compuesto=ap_compuesto, tiempo=tiempo, radical=radical, pocp_compuesto=pocp_compuesto, gwp_covs_20=gwp_covs_20, gwp_covs_100=gwp_covs_100, gwp_covs_500=gwp_covs_500)

#Ruta para calcular el AP
@app.route('/potencial_ap', methods=['GET', 'POST'])
def potencial_acido():
    if request.method == 'POST':
        abreviatura = request.form['compuesto']
        peso_molecular_cov = float(request.form['peso_molecular'])
        cloro = int(request.form['cloro'])
        fluor = int(request.form['fluor'])
        nitrogeno = int(request.form['nitrogeno'])
        azufre = int(request.form['azufre'])
        ap, lista = impactos.potencial_acidificacion(peso_molecular_cov, cloro, fluor, nitrogeno, azufre)
        compuestos.modify(ap, abreviatura)#Ingreso los datos calculados en la base de datos
        return render_template('acidificacion.html', ap=ap, lista=lista, abreviatura=abreviatura)  
    return render_template('acidificacion.html')


#Ruta para calcular el AP
@app.route('/potencial_pocp', methods=['GET', 'POST'])
def potencial_o3():
    if request.method == 'POST':
        abreviatura = request.form['abreviatura']
        carbonos = int(request.form['carbonos'])
        enlaces = int(request.form['enlaces'])
        peso_molecular = float(request.form['peso_molecular'])
        koh_compuesto = float(request.form['koh_cov'])
        koh_producto = float(request.form['koh_producto'])
        rendimiento = float(request.form['rendimiento'])
        ko3_compuesto = float(request.form['ko3_cov'])
        dato_a = str(request.form.get('multiplicador_a'))
        dato_p = str(request.form.get('dato_p'))
        dato_ro3 = str(request.form.get('dato_ro3'))
        dato_q = str(request.form.get('dato_q'))
        if dato_q == 'N/A':
            dato_q = 0
        if dato_p == 'N/A':
            dato_p = 0
        if dato_ro3 == 'N/A':
            dato_ro3 = 0
        region = str(request.form.get('region'))
        
        pocp = impactos.potencial_ozono(dato_a, enlaces, peso_molecular, carbonos, koh_compuesto, ko3_compuesto, koh_producto, rendimiento, dato_p, dato_ro3, dato_q, region)
        compuestos.modify_pocp(pocp, abreviatura)#Ingreso los datos calculados en la base de datos
        return render_template('estimaozono.html', pocp=pocp, abreviatura=abreviatura)  
    return render_template('estimaozono.html')

#Ruta para calcular el tiempo de residencia atmosférico
@app.route('/residencia_t', methods=['GET', 'POST'])
def residencia_t():
    if request.method == 'POST':
        k_compuesto = float(request.form['k_cov'])
        compuesto_cov = request.form['compuesto']
        radical = str(request.form.get('radicales'))
        tiempo = round((impactos.tiempo_residencia(k_compuesto, radical)) / 3600, 2)
        compuestos.modify_t(tiempo, radical, compuesto_cov)#Ingreso los datos calculados en la base de datos
        return render_template('residencia.html', compuesto_cov=compuesto_cov, tiempo=tiempo, radical=radical)
    return render_template('residencia.html')

#Ruta para calcular los GWP con un archivo que suministra el usuario
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        archivo_gwp = request.files['csvfile']
        data = pd.read_csv(archivo_gwp)
        lista_onda = list(data['cm-1'])
        lista_abs = list(data['abs'])
        koh_cov = float(request.form['koh_cov'])
        kcl_cov = float(request.form['kcl_cov'])
        ko3_cov = float(request.form['ko3_cov'])
        concentracion = float(request.form['concentracion'])
        abreviatura = request.form['abreviatura']
        paso_optico = float(request.form['paso_optico'])
        peso_molecular = float(request.form['peso_molecular'])
        tiempo_oh = (impactos.tiempo_residencia(koh_cov,'OH'))/(3600 * 24)
        tiempo_cl = (impactos.tiempo_residencia(kcl_cov,'Cl'))/(3600 * 24)
        tiempo_o3 = (impactos.tiempo_residencia(ko3_cov,'O3'))/(3600 * 24)
        #Hacer un vector de la referencia de CO2
        with open('referencia_co2.csv') as csvfile: #Leo el archivo tipo diccionario
            diccionario_secciones = list(csv.DictReader(csvfile))
        columna_co2 = "f_105"
        lista_co2 = []
        for i in range(len(diccionario_secciones)):
            lista_co2.append(diccionario_secciones[i][columna_co2])
        lista_sint = []
        for i in range(len(lista_abs)):
            lista_sint.append((float(lista_abs[i]) / (concentracion * paso_optico)) * 2.303)
        lista_f_sint =[]
        for i in range(len(lista_co2)):
            lista_f_sint.append(float(lista_co2[i]) * float(lista_sint[i]) * 1E15 * 2.303)
        if tiempo_o3 != 0:#En éste caso es porque el compuesto es saturado
            time_years = (1/((1 / tiempo_oh) + (1 / tiempo_cl) + (1 / tiempo_o3))) / 365
        else:
            time_years = (1/((1 / tiempo_oh) + (1 / tiempo_cl))) / 365 #Compuestos Insaturados
        funcion_tiempo = ((2.962*(time_years ** 0.9312))/(1+(2.994*(time_years ** 0.9302))))
        lista_nueva = []
        for i in range(2500):#Solo se necesita hasta 2500 valores
            lista_nueva.append(lista_f_sint[i])
        rf_ghg = sum(lista_nueva)
        rf_corrected = rf_ghg * funcion_tiempo
        gwp_20 = (rf_corrected*(28.97/peso_molecular)*(1E9/5.135E18)*time_years*(1-(math.exp(-20/time_years)))) / 2.495E-14
        gwp_100 = (rf_corrected*(28.97/peso_molecular)*(1E9/5.135E18)*time_years*(1-(math.exp(-100/time_years)))) / 9.171E-14   
        gwp_500 = (rf_corrected*(28.97/peso_molecular)*(1E9/5.135E18)*time_years*(1-(math.exp(-500/time_years)))) / 3.217E-13
        compuestos.modify_gwp(gwp_20, gwp_100, gwp_500, abreviatura)
        return redirect(url_for('indices'))
    return render_template('gwp.html')


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True)#Se encarga de ejecutar el servidor (5000)
                    #Al colocar True los cambios que haga en el codigo
                    #Se ven automaticamente en la pagina
                    #Si coloco False por mas cambios que haga no se vera
    
    