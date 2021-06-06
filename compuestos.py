#!/usr/bin/env python
'''
Impactos Ambientales
---------------------------
Autor: Pedro Luis Lugo Garcia
Version: 1.0
 
Descripcion:
Programa creado para determinar las propiedades
de compuestos organicos volatiles a estudiar en la atmosfera.
'''

__author__ = "Pedro Luis Lugo Garcia"
__email__ = "pedro.lugo@unc.edu.ar"
__version__ = "1.0"


import sqlite3
import matplotlib.pyplot as plt
import matplotlib.axes
import matplotlib.gridspec as gridspec

def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('compuestos.db')

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Ejecutar una query
    c.execute("""
                DROP TABLE IF EXISTS compuestos;
            """)

    # Ejecutar una query
    c.execute("""
            CREATE TABLE compuestos(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [formula] TEXT NOT NULL,
                [nombre] TEXT NOT NULL,
                [abreviatura] TEXT NOT NULL,
                [densidad] DECIMAL,
                [peso_molecular] DECIMAL,
                [sustituyentes] TEXT NOT NULL,
                [enlace] TEXT NOT NULL,
                [k_oh] DECIMAL,
                [t_oh] DECIMAL,
                [k_cl] DECIMAL,
                [t_cl] DECIMAL,
                [k_no3] DECIMAL,
                [t_no3] DECIMAL,
                [k_o3] DECIMAL,
                [t_o3] DECIMAL,
                [ap_cov] DECIMAL,
                [pocp_cov] DECIMAL,
                [gwp_20] DECIMAL,
                [gwp_100] DECIMAL,
                [gwp_500] DECIMAL
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

def insert_compuestos(formula, nombre, abreviatura, densidad, peso_molecular, sustituyentes, enlace, k_oh, t_oh, k_cl, t_cl, k_no3, t_no3, k_o3, t_o3, ap_cov, pocp_cov, gwp_20, gwp_100, gwp_500):
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()

    values = [formula, nombre, abreviatura, densidad, peso_molecular, sustituyentes, enlace, k_oh, t_oh, k_cl, t_cl, k_no3, t_no3, k_o3, t_o3, ap_cov, pocp_cov, gwp_20, gwp_100, gwp_500]

    c.execute("""
        INSERT INTO compuestos (formula, nombre, abreviatura, densidad, peso_molecular, sustituyentes, enlace, k_oh, t_oh, k_cl, t_cl, k_no3, t_no3, k_o3, t_o3, ap_cov, pocp_cov, gwp_20, gwp_100, gwp_500)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", values)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

def insert_grupo(group):
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()


    c.executemany("""
        INSERT INTO compuestos (formula, nombre, abreviatura, densidad, peso_molecular, sustituyentes, enlace, k_oh, t_oh, k_cl, t_cl, k_no3, t_no3, k_o3, t_o3, ap_cov, pocp_cov, gwp_20, gwp_100, gwp_500)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", group)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

def modify(ap_cov, abreviatura):
    print('Modificando la tabla')
     # Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()

    rowcount = c.execute("UPDATE compuestos SET ap_cov =? WHERE abreviatura =?",
                         (ap_cov, abreviatura)).rowcount

    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

def modify_pocp(pocp_cov, abreviatura):
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()
    row = c.execute("UPDATE compuestos SET pocp_cov =? WHERE abreviatura =?",
                    (pocp_cov, abreviatura))
    
    conn.commit()
    conn.close()

def modify_t(tiempo, radical, abreviatura):
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()
    if radical == "OH":
        row = c.execute("UPDATE compuestos SET t_oh =? WHERE abreviatura =?",
                    (tiempo, abreviatura))
    else:
        if radical == "Cl":
            row = c.execute("UPDATE compuestos SET t_cl =? WHERE abreviatura =?",
                    (tiempo, abreviatura))
        else:
            if radical == "NO3":
                row = c.execute("UPDATE compuestos SET t_no3 =? WHERE abreviatura =?",
                    (tiempo, abreviatura))
            else:
                row = c.execute("UPDATE compuestos SET t_o3 =? WHERE abreviatura =?",
                    (tiempo, abreviatura))
    conn.commit()
    conn.close()

def modify_gwp(gwp_20, gwp_100, gwp_500, abreviatura):
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()
    row = c.execute("UPDATE compuestos SET gwp_20 =? WHERE abreviatura =?",
                    (gwp_20, abreviatura))
    row = c.execute("UPDATE compuestos SET gwp_100 =? WHERE abreviatura =?",
                    (gwp_100, abreviatura))
    row = c.execute("UPDATE compuestos SET gwp_500 =? WHERE abreviatura =?",
                    (gwp_500, abreviatura))
    conn.commit()
    conn.close()

def show():
    # Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()


    # Leer todas las filas y obtener los datos de a uno
    c.execute('SELECT * FROM compuestos')
    for row in c.execute('SELECT * FROM compuestos'):
        print(row)

    # Cerrar la conexión con la base de datos
    conn.close()


def busqueda_compuestos(abreviatura):
    # Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()
    lista = []
    for row in c.execute('SELECT peso_molecular, k_oh FROM compuestos WHERE abreviatura = :abreviatura', {'abreviatura': abreviatura}):
        lista.append(row)
    conn.close()
    return lista[0], lista[1]


def busqueda_ap():
    #Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()
    lista_cov = []
    for row in c.execute('SELECT abreviatura, ap_cov FROM compuestos'):
        lista_cov.append(row)
    resultado = []
    covs = []
    ap = []
    for i in range(len(lista_cov)):
        resultado = list(lista_cov[i])
        covs.append(resultado[0])
        ap.append(resultado[1])
    conn.close()
    return covs, ap


def busqueda_pocp():
    # Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()
    lista_cov = []
    for row in c.execute('SELECT abreviatura, pocp_cov FROM compuestos'):
        lista_cov.append(row)
    resultado = []
    covs = []
    pocp = []
    for i in range(len(lista_cov)):
        resultado = list(lista_cov[i])
        covs.append(resultado[0])
        pocp.append(resultado[1])
    conn.close()
    return covs, pocp


def delete_compuesto(abreviatura):
    # Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()

    # NOTA: Recordar que las tupla un solo elemento se definen como
    # (elemento,)
    # Si presta a confusión usar una lista --> [elemento]
    rowcount = c.execute("DELETE FROM compuestos WHERE abreviatura =?", (abreviatura,)).rowcount

    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()



create_schema()
group = [("CH2=C(CH3)C(O)OCH2(CF3)","2,2,2-Trifluoroethyl methacrylate", "TFEM", 1.181, 168.11, "Fluorado", "Insaturado", 1.70E-11, 8.16, 2.22E-10, 125.12, 0, 0, 1.14E-17, 34.80, 0.81, 46.66, 0.000, 0.000, 0.000),
             ("CH2=CHC(O)OCH(CF3)2", "1,1,1,3,3,3-Hexafluoroisopropyl acrylate", "HFIA", 1.33, 222.09, "Fluorado", "Insaturado", 1.22E-11, 11.38, 1.39E-10, 199.84, 0, 0, 1.14E-17, 34.80, 0.57, 53.30, 0.003, 0.001, 0.000),
             ("CH2=C(CH3)C(O)OCH(CF3)2", "1,1,1,3,3,3-Hexafluoroisopropyl methacrylate", "HFIM", 1.302, 236.11, "Fluorado", "Insaturado", 1.67E-11, 8.31, 2.44E-10, 113.84, 0, 0, 1.75E-18, 226.75, 0.86, 34.34, 0.002, 0.001, 0.000),
             ("CH2=CHC(O)OCH2CF3", "2,2,2-Trifluoroethyl acrylate", "TFEA", 1.216, 154.09, "Fluorado", "Insaturado", 1.53E-11, 9.07, 2.41E-10, 115.26, 0, 0, 1.75E-18, 226.75, 0.62, 43.59, 0.003, 0.001, 0.000),
             ]
insert_grupo(group)


