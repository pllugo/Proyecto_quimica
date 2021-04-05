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

import impactos
import compuestos

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acidificacion.db'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('portada.html')

#@app.route('/compuesto_cov', methods=['GET', 'POST'])
#def add_compuesto():
 #   if request.method == 'GET':
  #      return render_template('index.html')

   # if request.method == 'POST':
    #    compuesto = request.form['compuesto']
     #   densidad_cov, peso_molecular_cov = compuestos.busqueda_covs(compuesto)
      #  print('La densidad del compuesto es {} (g/mL) y el peso molecular es {} (g/mol)'.format(densidad_cov, peso_molecular_cov))
       # return redirect(url_for('potencial_acido'))

@app.route('/acidificacion', methods=['GET', 'POST'])
def potencial_acido():
    if request.method == 'GET':
        return render_template('indices.html')
    
    if request.method == 'POST':
        compuesto = request.form['compuesto']
        cloro = int(request.form['cloro'])
        fluor = int(request.form['fluor'])
        nitrogeno = int(request.form['nitrogeno'])
        azufre = int(request.form['azufre'])
        densidad_cov, peso_molecular_cov = compuestos.busqueda_covs(compuesto)
        print('La densidad del compuesto es {} (g/mL) y el peso molecular es {} (g/mol)'.format(densidad_cov, peso_molecular_cov))
        ap, lista = impactos.potencial_acidificacion(peso_molecular_cov, cloro, fluor, nitrogeno, azufre)
        print(ap)
        print(lista)
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True)#Se encarga de ejecutar el servidor (5000)
                    #Al colocar True los cambios que haga en el codigo
                    #Se ven automaticamente en la pagina
                    #Si coloco False por mas cambios que haga no se vera
    
    