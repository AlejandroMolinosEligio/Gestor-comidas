import random
from datetime import date,timedelta

lista_comidas = []
lista_dias = ['Lunes','Martes','Miercoles', 'Jueves','Viernes','Sabado','Domingo']


with open('./Comidas.txt') as f:
    for linea in f:
        lista_comidas.append(linea[:-1])

random.shuffle(lista_comidas)

lista_dias = 2*lista_dias

if('Croquetas' in lista_comidas[:14] and 'Puchero' in lista_comidas[:14]):
    indexCroquetas =lista_comidas[:14].index('Croquetas')
    indexPuchero = lista_comidas[:14].index('Puchero')
    if indexCroquetas<indexPuchero:
        lista_comidas[indexCroquetas] = 'Puchero'
        lista_comidas[indexPuchero] = 'Croquetas'


hoy = date.today()
hoy = hoy +timedelta(days=1)
fichero = 'Lista 2 semanas - '+str(hoy)+'.txt'
file = open(fichero,'w')
file = open(fichero,'a')
for dia,comida in zip(lista_dias,lista_comidas[:14]):
    file.write(dia+" "+str(hoy.day)+':\n'+comida+"\n\n")
    hoy = hoy +timedelta(days=1)

file.close()