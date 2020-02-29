#   Benemérita Universidad Autónoma de Puelba
#   Facultad de Ciencias de la Computación
#   Sistemas Operativos II
#
#   Simulador de Despachador Híbrido + Administración de Memoria por Paginación
#   con Intercambio de páginas
#   Lotería-Prioridades + CLOCK_DWF
#   
#   Arizmendi Ramírez Esiel Kevin
#   Coria Rios Marco Antonio
#
#   Primavera 2020
#     lock.release()

from time import sleep
from random import randint
from common import MINPROCESS, MAXPROCESS

MINSLEEP = 10
MAXSLEEP = 15
FILENAME = "input.txt"

def charge(shlist, lock, fband):
    # Lísta de procesos leídos desde el archivo (se invierte para enviar del 1 a ...)
    rawproclist = getrawproc()[::-1]

    # Agrega los procesos a la memoria compartida
    while rawproclist:
        lock.acquire()
        for i in range(randint(MINPROCESS, MAXPROCESS)):
            if rawproclist: shlist.put(rawproclist.pop()) 
            else: break
        lock.release()

        sleep(randint(MINSLEEP, MAXSLEEP))
    
    lock.acquire()
    fband.value = 1
    lock.release()


# Lee el archivo y obtiene la información de los procesos
def getrawproc():
    rawproclist = []
    try:
        f = open(FILENAME, 'r')
        for line in f:
            rawproclist.append(line.replace('\n', ''))

        return rawproclist
    except:
        print('Error al abrir el archivo')
        exit()
