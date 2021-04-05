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

import sqlite3


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('parametros_pocp.db')

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Ejecutar una query
    c.execute("""
                DROP TABLE IF EXISTS parametros_pocp;
            """)

    # Ejecutar una query
    c.execute("""
            CREATE TABLE parametros_pocp(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [clase_cov] TEXT NOT NULL,
                [condiciones_europa] DECIMAL,
                [condiciones_usa] DECIMAL
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

def insert_compuestos(clase_cov, condiciones_europa, condiciones_usa):
    conn = sqlite3.connect('parametros_pocp.db')
    c = conn.cursor()

    values = [clase_cov, condiciones_europa, condiciones_usa]

    c.execute("""
        INSERT INTO parametros_pocp (clase_cov, condiciones_europa, condiciones_usa)
        VALUES (?,?,?);""", values)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

def insert_grupo(group):
    conn = sqlite3.connect('parametros_pocp.db')
    c = conn.cursor()

    c.executemany("""
        INSERT INTO parametros_pocp (clase_cov, condiciones_europa, condiciones_usa)
        VALUES (?,?,?);""", group)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def show():
    # Conectarse a la base de datos
    conn = sqlite3.connect('parametros_pocp.db')
    c = conn.cursor()

    # Leer todas las filas y obtener los datos de a uno
    c.execute('SELECT * FROM parametros_pocp')
    for row in c.execute('SELECT * FROM parametros_pocp'):
        print(row)

    # Cerrar la conexión con la base de datos
    conn.close()


def busqueda_parametro(clase_cov, condiciones):
    # Conectarse a la base de datos
    conn = sqlite3.connect('parametros_pocp.db')
    c = conn.cursor()
    lista = []
    if condiciones =='europa':
        for row in c.execute('SELECT condiciones_europa FROM parametros_pocp WHERE clase_cov=:clase_cov', {'clase_cov': clase_cov}):
           lista.append(row)
    else:
        if condiciones == 'usa':
            for row in c.execute('SELECT condiciones_usa FROM parametros_pocp WHERE clase_cov =?', (clase_cov,)):
                lista.append(row)
        else:
            print('No existe esas condiciones')
    

    
    # Cerrar la conexión con la base de datos
    conn.close()
    return lista


def delete_compuesto(clase_cov):
    # Conectarse a la base de datos
    conn = sqlite3.connect('parametros_pocp.db')
    c = conn.cursor()

    # Borrar la fila cuyo nombre coincida con la búsqueda
    # NOTA: Recordar que las tupla un solo elemento se definen como
    # (elemento,)
    # Si presta a confusión usar una lista --> [elemento]
    rowcount = c.execute("DELETE FROM parametros_pocp WHERE clase_cov =?", (clase_cov,)).rowcount

    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()

create_schema()
group = [("alifaticos", 100, 154),
             ("aromaticos con 0 sustituyentes alquilos", 66, 25),
             ("aromaticos con 1 sustituyentes alquilos", 130, 320),
             ("aromaticos con 2 sustituyentes alquilos", 173, 427),
             ("aromaticos con 3 sustituyentes alquilos", 206, 509),
             ("B", 4, 1),
             ("alfa", 0.56, 0.37),
             ("C", 0.0038, 0.0041),
             ("beta",2.7,2.7),
             ("alifaticos", 0.38, 0.25),
             ("alifaticos", 0.16, 0.18),
             ("aldehidos y cetonas", 14, 10),
             ("alfa-dicarbonilos", 67, 124),
             ("ciclocetonas", 0, 0),
             ("alquenos y oxigenados insaturados", 20.9, 22),
             ("alquenos y oxigenados insaturados", 0.043, 0.15),
             ("benzaldehidos y estirenos", 74, 80),
             ("hidroxiarenos", 41, 0),
             ]
insert_grupo(group)


