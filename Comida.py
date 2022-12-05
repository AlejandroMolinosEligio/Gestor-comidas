import sqlite3
import random
from datetime import date,timedelta
import datetime

## CLASES

class Comida:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        

    def saludar(self):
        print("Hola mundo"+self.name)


class Ingrediente:

    def __init__(self, name, date, status, disponibility, amount):
        self.name = name
        self.date = date
        self.status = status
        self.disponibility = disponibility
        self.amount = amount

## BASE DE DATOS
        
def creacionDB():
    conexion=sqlite3.connect("example.db")
    try:
        conexion.execute("""create table meal (
                                id integer primary key autoincrement,
								name text,
								ingredients text
								);
                            """)

        conexion.execute("""create table ingredient (
                                id integer primary key autoincrement,
								name text,
								date DATE,
                                status text DEFAULT 'OK',
                                disponibility text DEFAULT 'NO',
                                amount integer
                            );
                            """)

        print("se creo la tabla articulos")                        
    except sqlite3.OperationalError:
        print("La tabla articulos ya existe")                    
    conexion.close()

def addComidas():

    fichero = "ComidasDB.txt"
    conexion=sqlite3.connect("example.db")
    cursor = conexion.cursor()
    with open('./'+fichero) as f:
        for linea in f:
            name = linea[:-1].split(";")[0]
            lista = linea[:-1].split(";")[1]
            try:
                sql = """INSERT INTO meal(name,ingredients) VALUES ("{}","{}")
                """.format(name,lista)
                cursor.execute(sql)
                conexion.commit()
            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)                 

    conexion.close()

def addIngredients():

    fichero = "IngredientesDB.txt"
    conexion=sqlite3.connect("example.db")
    cursor = conexion.cursor()
    with open('./'+fichero) as f:
        for linea in f:
            linea = linea[:-1].split(",")
            try:
                sql = """INSERT INTO ingredient(name,date,status,disponibility,amount) VALUES ("{}",{},"{}","{}",{})
                """.format(linea[0],linea[1],linea[2],linea[3],linea[4])
                print(sql)
                cursor.execute(sql)
                conexion.commit()
            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)                 

    conexion.close()

## CARGAR DATOS

def loadComidas():

    conexion=sqlite3.connect("example.db")
    cur = conexion.cursor()
    cur.execute("SELECT name,ingredients FROM meal")

    rows = cur.fetchall()

    lista = []

    for row in rows:
        comida = Comida(row[0],row[1])
        lista.append(comida)
    
    return lista

def checkIngredients(listIngradients):

    conexion=sqlite3.connect("example.db")
    cur = conexion.cursor()
    lista = []

    for item in listIngradients:

        cur.execute('SELECT name,date,status,disponibility,amount FROM ingredient WHERE name="{}"'.format(item))

        rows = cur.fetchall()

        for row in rows:
            ingredient = Ingrediente(row[0],row[1],row[2],row[3],row[4])
            lista.append(ingredient)
    
    return lista

## RANDOM

def generateRandomList(lista_comidas_obj, lista_comidas):

    lista_dias = ['Lunes','Martes','Miercoles', 'Jueves','Viernes','Sabado','Domingo']
    random.shuffle(lista_comidas)

    lista_dias = 2*lista_dias

    hoy = date.today()
    hoy = hoy +timedelta(days=1)
    fichero = 'Lista 2 semanas - '+str(hoy)+'.txt'


    if('Croquetas' in lista_comidas[:14] and 'Puchero' in lista_comidas[:14]):
        indexCroquetas =lista_comidas[:14].index('Croquetas')
        indexPuchero = lista_comidas[:14].index('Puchero')
        if indexCroquetas<indexPuchero:
            lista_comidas[indexCroquetas] = 'Puchero'
            lista_comidas[indexPuchero] = 'Croquetas'

    file = open(fichero,'w')
    file = open(fichero,'a')

    check = True

    for dia,comida in zip(lista_dias,lista_comidas[:14]):

        meal = None
        for name in lista_comidas_obj:
            if(name.name == comida):
                meal = name
                break
        
        lista_ingredientes = checkIngredients(meal.ingredients[1:].split(", "))
        if(not checkCaducidad(hoy,lista_ingredientes)): 
            check = False
            break

        file.write(dia+" "+str(hoy.day)+':\n'+comida+"\n\n")
        hoy = hoy +timedelta(days=1)


    file.close()

    if(not check):
        generateRandomList(lista_comidas_obj, lista_comidas)

    return 0

def checkCaducidad(current,lista_ingredientes):

    check = True
    
    for ingredient in lista_ingredientes:

            if ingredient.date != None:
                lista = [int(item) for item in ingredient.date.split("-")]
                fecha = datetime.date(lista[0],lista[1],lista[2])
                if current>fecha:
                    check = False
                    print("Dia de la comida",current)
                    print("Fecha caducidad", fecha)
                    break

    return check

## PRINCIPAL

def main():

    lista_comidas_obj = loadComidas()
    lista_comidas = [item.name for item in lista_comidas_obj]

    generateRandomList(lista_comidas_obj,lista_comidas)
    
    



if __name__ == "__main__":
    main()