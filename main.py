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

import multiprocessing 
import charger
import dispatcher
from common import MAXPROCESS

if __name__ == "__main__": 
    # Creando los elementos en común (memoria, bandera de paro, semáforo)
    shlist = multiprocessing.Queue()
    fband = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
  
    # creating new processes 
    p1 = multiprocessing.Process(target=charger.charge, args=(shlist,lock,fband)) 
    p2 = multiprocessing.Process(target=dispatcher.dispatch, args=(shlist,lock,fband)) 
  
    # running processes 
    p1.start() 
    p2.start()
  
    # wait until processes finish 
    p1.join() 
    p2.join()