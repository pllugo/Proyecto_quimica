#!/usr/bin/env python
'''
Impactos Ambientales
---------------------------
Autor: Pedro Luis Lugo Garcia
Version: 1.0
 
Descripcion:
Programa creado para calcular los impactos ambientales de
compuestos organicos volátiles (COVs) en el aire.
'''

__author__ = "Pedro Luis Lugo Garcia"
__email__ = "pedro.lugo@unc.edu.ar"
__version__ = "1.0"

import sqlite3


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('acidificacion.db')

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Ejecutar una query
    c.execute("""
                DROP TABLE IF EXISTS acidificacion;
            """)

    # Ejecutar una query
    c.execute("""
            CREATE TABLE acidificacion(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [compuestos] TEXT NOT NULL,
                [potenciales] DECIMAL
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

def insert_compuestos(compuestos, potenciales):
    conn = sqlite3.connect('acidificacion.db')
    c = conn.cursor()

    values = [compuestos, potenciales]

    c.execute("""
        INSERT INTO acidificacion (compuestos, potenciales)
        VALUES (?,?);""", values)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

def insert_grupo(group):
    conn = sqlite3.connect('acidificacion.db')
    c = conn.cursor()

    c.executemany("""
        INSERT INTO acidificacion (compuestos, potenciales)
        VALUES (?,?);""", group)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def show():
    # Conectarse a la base de datos
    conn = sqlite3.connect('acidificacion.db')
    c = conn.cursor()


    # Leer todas las filas y obtener los datos de a uno
    c.execute('SELECT * FROM acidificacion')
    for row in c.execute('SELECT * FROM acidificacion'):
        print(row)

    # Cerrar la conexión con la base de datos
    conn.close()


def busqueda_compuestos_potenciales(potenciales):
    # Conectarse a la base de datos
    conn = sqlite3.connect('acidificacion.db')
    c = conn.cursor()
    lista = []
    if potenciales >= 0.5 and potenciales <= 1:
        for row in c.execute('SELECT compuestos, potenciales FROM acidificacion WHERE potenciales <= :potenciales OR potenciales <= :Potenciales', {'potenciales': potenciales, 'Potenciales': 0.7}):
            lista.append(row)
    else:
        if potenciales >= 0.5 and potenciales >= 1:
            for row in c.execute('SELECT compuestos, potenciales FROM acidificacion WHERE potenciales >= :potenciales', {'potenciales': potenciales}):
                lista.append(row)
        else:
            print('El Ap es bajo')
    conn.close()
    return lista


def delete_compuesto(compuestos):
    # Conectarse a la base de datos
    conn = sqlite3.connect('acidificacion.db')
    c = conn.cursor()

    # Borrar la fila cuyo nombre coincida con la búsqueda
    # NOTA: Recordar que las tupla un solo elemento se definen como
    # (elemento,)
    # Si presta a confusión usar una lista --> [elemento]
    rowcount = c.execute("DELETE FROM acidificacion WHERE compuestos =?", (compuestos,)).rowcount

    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()



create_schema()
#La lista a ingresar funciona como referencia
#para comparar el COV con el AP del grupo ingresado
group = [('SO2', 1.0),
             ('NO', 1.07),
             ('NO2', 0.7),
             ('NOX', 0.7),
             ('NH3', 1.88),
             ('HCl', 0.88),
             ('HF', 1.6),
             ]
insert_grupo(group)






