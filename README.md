# App Química Atmosférica (Impactos Ambientales) 📊 🏭

Este es un proyecto de creación de una app para conocer los impactos ambientales (Potencial de Acidificación (AP), Potencial de Creación de Ozono troposferico (POCP), tiempo de residencia atmosférico y Potencial de Calentamiento Global (GWP)) de un compuesto orgánico volatil (COV) en la atmósfera.

## Metodologia Experimental

### Potencial de Acidificación
La oxidación troposférica de compuestos orgánicos volátiles que contienen Cl, F, N o S en sus estructuras químicas también podría contribuir a la acidificación atmosférica, ya que generalmente producen especies ácidas (de Leeuw, 1993), ácidos carboxílicos, que particularmente llegan al suelo en deposición húmeda. procesos con muy alta capacidad de lavado (de Leeuw, 1993), por lo que el AP viene dado por:

![image](https://user-images.githubusercontent.com/72478141/120937147-29bb9580-c6e2-11eb-865f-b3c81ab8cccc.png)

* n: El número de átomos de Cl, F, N y S en una molécula.
* MSO2 Peso molecular SO2
* MCOVs Peso molecular del COV

### Potencial de Creación de Ozono Troposferico
Una forma de estudiar la posible formación de Ozono troposférico de un COV en el aire, es a traves del estudio del calculo del POCP

![image](https://user-images.githubusercontent.com/72478141/120937476-009c0480-c6e4-11eb-9f2d-786fe93cf995.png)

![image](https://user-images.githubusercontent.com/72478141/120937643-fe867580-c6e4-11eb-941e-956729cbdf14.png)

![image](https://user-images.githubusercontent.com/72478141/120937682-2d045080-c6e5-11eb-9d97-983a408857bc.png)



### Tiempo de residencia atmosférico

Uno de los parámetros que dan mucha información acerca de los posibles impactos ambientales de un COV en la atmosfera es el tiempo de residencia atmosferico, el cual relaciona la constante cinética del compuesto con la concentración del oxidante, ya sea, radicales OH*, Cl, NO3 y O3. Asi se conoce si el COV tiene un impacto local, regional o mayor.

 ### Técnias de medición (datos)

1. FTIR: Espectroscopía Infrarroja con Transformada de Fourier
2. GC-FID: Cromatografía Gaseosa con Detector de Llama

# Pre-requisitos de la app 📋

La app requiere la instalación de las siguientes librerias:

* import numpy as np
* import csv
* import sqlite3
* import traceback
* import io
* import sys
* import os
* import base64
* import json
* from datetime import datetime, timedelta
* import pandas as pd
* import math

* from flask import Flask, request, jsonify, render_template, Response, redirect , url_for, session
* from flask_sqlalchemy import SQLAlchemy
* import matplotlib
* matplotlib.use('Agg')  
* import matplotlib.pyplot as plt
* from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
* from matplotlib.figure import Figure
* import matplotlib.image as mpimg
 


### Estructura de la App Química Atmosférica ⌨

- _app_ : El programa app es donde se desarrolla la parte central de la aplicación y llama a las demás funciones, métodos, etc.
- _impactos_ : El programa impactos se crea para calcular los diferentes impactos como son: AP, POCP y tiempo de residencia de un COV en la atmosfera.
- _compuestos_: Este programa se crea para determinar las propiedades de compuestos organicos volatiles a estudiar en la atmosfera, para ello crea y se conecta a una base de  datos.
- _parámetros_acidificacion_:Programa creado para crear una base datos de potencial de creación de ozono troposférico de compuestos organicos volátiles (COVs) en el aire.
- _parámetros_ozono_: Programa creado para crear una base datos de potenciales de acidificación de un COV teniendo como referencia un grupo de compuestos como el SO2, NO2, NOx, NH3, HCl y HF en el aire.

### Datos de entrada de la App 💻

1. Se debe dar click al boton que dice Datos COV y colocar los datos del compuesto como aparece en la imagen, luego dar click en el boton Ingresar

![image](https://user-images.githubusercontent.com/72478141/120936250-4dc8a800-c6dd-11eb-8bb8-48a20130d1c7.png)

2. Luego automaticamente la app lleva a la pagina de potencial de acidificacion donde hay que ingresar los datos que alli se piden

![image](https://user-images.githubusercontent.com/72478141/120936361-c465a580-c6dd-11eb-933c-c09262ffa289.png)

3. Al dar click en el boton Calcular arrojara en la parte inferior los resultados de AP

![image](https://user-images.githubusercontent.com/72478141/120936423-04c52380-c6de-11eb-808c-128bf3f77d10.png)

4. El siguiente paso es calcular los POCP para ello debe dar click en el boton de Potencial POCP, ingresar los datos como en pantalla y presionar Calcular

![image](https://user-images.githubusercontent.com/72478141/120936456-3b02a300-c6de-11eb-99f6-a59533ffc04e.png)

![image](https://user-images.githubusercontent.com/72478141/120936498-7309e600-c6de-11eb-9fd1-675f9b638847.png)

![image](https://user-images.githubusercontent.com/72478141/120936516-8cab2d80-c6de-11eb-9061-83cd9602b269.png)

![image](https://user-images.githubusercontent.com/72478141/120936552-c9772480-c6de-11eb-90cf-aed894020ec6.png)

5. Ahora hay que dar click en el boton de tiempo de residencia, ingresar los datos y presionar Calcular

![image](https://user-images.githubusercontent.com/72478141/120936597-fdeae080-c6de-11eb-8f0f-bae1ae9067a6.png)

![image](https://user-images.githubusercontent.com/72478141/120936610-122edd80-c6df-11eb-8ee7-8d894b761631.png)

6. El ultimo parámetro para calcular es el Potencial de Calentamiento Global (GWP) presionamos el boton GWP e ingresamos los datos. Hay que tener en cuenta, que el archivo de datos para el cálculo del GWP debe estar en formato .csv

![image](https://user-images.githubusercontent.com/72478141/120936657-4e623e00-c6df-11eb-9bfc-4987803033cf.png)

7. Al dar click en el boton de Calcular, el programa arroja la siguiente pagina

![image](https://user-images.githubusercontent.com/72478141/120936715-aac55d80-c6df-11eb-85b7-f56977287745.png)

8. Para obtener los resultados en una sola pagina para una mejor experiencia del usuario y una visión amplia del COV a estudiar, se debe dar click al boton de Estadisticas y el programa arroja la siguiente información

![image](https://user-images.githubusercontent.com/72478141/120936781-02fc5f80-c6e0-11eb-9027-de0db6fd9861.png)

![image](https://user-images.githubusercontent.com/72478141/120936792-1ad3e380-c6e0-11eb-83c0-d32a076fbea9.png)

![image](https://user-images.githubusercontent.com/72478141/120936804-2cb58680-c6e0-11eb-9de8-54eb83949aaf.png)

# Notas Importantes 📉

1. El archivo a ingresar para calcular el GWP del compuesto a estudiar, debe estar en formato .csv y en la parte superior de las celdas debe contener cm-1 y abs debido a que el programa lee el archivo tipo diccionario.

![image](https://user-images.githubusercontent.com/72478141/120936878-a2215700-c6e0-11eb-89eb-0b79ead18fef.png)


2. Los botones como Tablero, Usuario y Perfil no se encuentran habilitados, ésto es porque la app esta diseñada para que otros becarios doctorales puedan mejorar el codigo de la presente app y actualizar las otras funciones que la app puede ofrecer. 

# Contribución 🚀

Esta app de química atmosferica orientado a los impactos ambientales que un Compuesto Orgánico Volátil (COV) puede ocasionar en la atmósfera, contribuye al estudio que actualmente se esta llevando acabo en los laboratorios: LUQCA de la Universidad Nacional de Córdoba (Argentina) y en BUW de la Universidad de Wuppertal (Alemania) y con la finalidad de que sea un área de investigación (simulaciones, data science, etc) en ambos centros de investigación de quimica atmosferica.

# Versión 📌

Versión 1.01

# Autor ✒

* MSc. Pedro Lugo
- Becario Doctoral CONICET-UNC







