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
                [nombre] TEXT NOT NULL,
                [formula] TEXT NOT NULL,
                [densidad] DECIMAL,
                [peso_molecular] DECIMAL
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

def insert_compuestos(nombre, formula, densidad, peso_molecular):
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()

    values = [nombre, formula, densidad, peso_molecular]

    c.execute("""
        INSERT INTO compuestos (nombre, formula, densidad, peso_molecular)
        VALUES (?,?,?,?);""", values)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

def insert_grupo(group):
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()

    c.executemany("""
        INSERT INTO compuestos (nombre, formula, densidad, peso_molecular)
        VALUES (?,?,?,?);""", group)

    conn.commit()
    # Cerrar la conexión con la base de datos
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


def busqueda_covs(nombre):
    # Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()

    
    for row in c.execute('SELECT densidad, peso_molecular FROM compuestos WHERE nombre =?', (nombre,)):
        densidad_covs = row[0]
        peso_molecular_covs = row[1]

    
    # Cerrar la conexión con la base de datos
    conn.close()
    return densidad_covs, peso_molecular_covs


def delete_compuesto(nombre):
    # Conectarse a la base de datos
    conn = sqlite3.connect('compuestos.db')
    c = conn.cursor()

    # Borrar la fila cuyo nombre coincida con la búsqueda
    # NOTA: Recordar que las tupla un solo elemento se definen como
    # (elemento,)
    # Si presta a confusión usar una lista --> [elemento]
    rowcount = c.execute("DELETE FROM compuestos WHERE nombre =?", (nombre,)).rowcount

    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

create_schema()
group = [("1,1,1-Trifluoro-2,4-pentanodiona", "CF3C(O)CH2C(O)CH3", 1.27, 154.09),
             ("1,1,1-Trifluoro-2,4-hexanodiona", "CF3C(O)CH2C(O)CH2CH3", 1.22, 168.11),
             ("1,1,1-Trifluoro-5-metil-2,4-hexanodiona", "CF3C(O)CH2C(O)CH(CH3)2", 1.2171, 182.14),
             ("Etil Fluoroacetato", "CH2FC(O)OCH2CH3", 1.098, 106.1),
             ]
insert_grupo(group)
