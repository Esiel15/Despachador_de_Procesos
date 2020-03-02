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

from random import randint
from time import sleep, time
from common import MINPROCESS, MAXPROCESS, MAX_DRAM, MAX_PCM, MAX_VM, Process, Page
from results import output

QUANTUM = 5 # Duración del Quantum
REFQ = 1 # Duración de la referencia

HOT_PAGE_THRESHOLD = 0
EXPIRATION = 8

# Varialbes Globales (!)
dram = []
pcm = []
vm = []

dram_index = 0
pcm_index = 0

# Variables estadísicas
refcount = 0 # Total de referencias hechas
pfcount = 0  # Total de fallos de página

def dispatch(shlist, lock, fband):
    global refcount
    
    # Variables del simulador
    proclist = []
    finished = []
    aniquilated = []
    active_proc = None
    numproc = 0
    q = 1

    start = time()

    while True:
        # Accede a la memoria compartida
        lock.acquire()
        # Verifica que aun deba continuar
        if fband.value == 1 and numproc == 0:
            print('Bye!')
            lock.release()
            break

        i = 0
        # Toma cada proceso en la memoria compartida y lo agrega a la lista
        # Agrega sus páginas a la memoria virtual
        while not shlist.empty():
            # Se obtiene un proceso de la lista compartida
            newproc = shlist.get()
            # Si ya no es posible asignarle memoria virtual, se aniquila
            if len(newproc.pagelist) > MAX_VM - len(vm):
                print("El proceso es demasiado grande\nNo se le puede asignar memoria. Aniquilando...")
                aniquilated.append(newproc)
            else:
                for page in newproc.pagelist:
                    vm.append(page)

                proclist.append(newproc)
                print(f'Added: {newproc.pid}\tVM : {MAX_VM - len(vm)}/{MAX_VM} frames restantes')
                i += 1
                numproc += 1
        lock.release()

        print('Loop')
        sleep(REFQ)

        # Si hay un proceso activo
        if active_proc != None:
            active_proc.show()

            # Conditional not working (!)
            
            if active_proc.refchain == '':
                print('Finished')
                # Elimina las páginas del proceso activo de las 3 memorias
                for page in active_proc.pagelist:
                    try:
                        dram.remove(page)
                        pcm.remove(page)
                    except:
                        pass
                    vm.remove(page)

                proclist.remove(active_proc)
                numproc -= 1
                finished.append(active_proc)
                active_proc = None

                if proclist:
                    active_proc = lottery(proclist)
                    #active_proc.show()
                    q = 0
                pass
            elif q == QUANTUM:
                active_proc = lottery(proclist)
                #active_proc.show()
                q = 0
            
            if numproc > 0:
                # Ejecutar página
                clockdwf(active_proc.nextpage(), randint(0, 1))
                q += REFQ
                updtwait(proclist, active_proc.pid)
                refcount += 1
            pass
        else:
            # Si aún quedan procesos disponibles
            if proclist:
                active_proc = lottery(proclist)
                #active_proc.show()
                q = 0

                # Ejecutar página
                clockdwf(active_proc.nextpage(), randint(0, 1))
                q += REFQ
                updtwait(proclist, active_proc.pid)
                refcount += 1
    
    end = time()

    systime = end - start
    output(finished, aniquilated, systime, refcount, pfcount)


# Calcula el total de tickets
# El total de tickets es la suma de todos las prioridades de todos los procesos
def tickets(proclist):
    ticketsum = 0
    for proc in proclist:
        ticketsum += proc.priority

    return ticketsum

# Selección del procesos a ejecutar por sorteo
# El número de tickets de un proces es igual a su prioridad
def lottery(proclist):
    T = tickets(proclist)

    print(f'Total Tickets: {T}')

    win = randint(1, T)

    print(f'Ganador: {win}')

    for proc in proclist:
        win -= proc.priority
        if win <= 0: return proc

# Actualiza los tiempos de espera para todos los procesos excepto el que se encuentra en ejecución
def updtwait(proclist, active_pid):
    for proc in proclist:
        if proc.pid != active_pid:
            proc.waittime += 1
        proc.totaltime += 1



# Algoritmo CLOCK-DWF
def clockdwf(page : Page, op) :
    global pfcount
    global dram
    global pcm

    if (page in dram) : #Si la pagina esta en dram 
        if (op == 0) : 
            page.r = 1 #Se cambia el bit R
        else: 
            page.m = page.r = 1 #Se cambia el bit R y M
    elif (page in pcm) : #Si la pagina esta en pcm
        if (op == 0) : 
            page.r = 1 #Se cambia el bit R
        else:
            free_frame_dram()
            dram.append(page) #Se agrega al final de la dram
            page.m = 0 #Se limpia el bit M
            print('\t--- Cambiada a la DRAM ---')
            print(f'\tDRAM: {MAX_DRAM - len(dram)}/{MAX_DRAM} frames disponibles.')
    else: #FALLO DE PÁGINA
        pfcount += 1
        print('\t--- Fallo de Página ---')
        opp = 'Lectura' if op == 0 else 'Escritura'
        print(f'\t--- Operación: {opp}')
        if (op == 0):
            free_frame_pcm() 
            pcm.append(page) #Se agrega al final de la pcm
            page.r = 0 #Se limpia el bit R
            print('\t--- Añadida ala PCM ---')
            print(f'\tPCM: {MAX_PCM - len(pcm)}/{MAX_PCM} frames disponibles.')
        else: #La operacion es escritura
            free_frame_dram()
            dram.append(page) #Se agrega al final de la dram
            page.m = 0 #Se limpia el M
            print('\t--- Añadida a la DRAM ---')
            print(f'\tDRAM: {MAX_DRAM - len(dram)}/{MAX_DRAM} frames disponibles.')


# Libera un marco de página de la DRAM
def free_frame_dram() :
    global dram
    global dram_index
    global pcm

    dramlen = len(dram)
    if dramlen == MAX_DRAM : #La dram ya esta llena
        while True:
            page = dram[dram_index] #La pagina apuntada por la manecilla
            if (page.m == 0): #La pagina no ha sido utilizada para escribir
                #Si la pagina es caliente y su centinela aún no llega al limite
                updhpt(page.frec) #Actualiza HOT_PAGE_THRESHOLD
                if (page.frec > HOT_PAGE_THRESHOLD and page.olr < EXPIRATION) :
                    page.olr += 1
                else: #La pagina es fria
                    dram.remove(page) 
                    if dram_index == dramlen : #Se removio la ultima página
                        dram_index = 0 #La manecilla apunta a la primer página
                    free_frame_pcm()
                    pcm.append(page) #Se añade la pagina al final de la pcm
                    page.m = 1 #El bit M se enciende para que se hagan los respaldos en DD una vez que esta en la pcm
                    print(f'\t--- Movida a la PCM (Proceso {page.owner.pid} Página {page.owner.pageindex(page)}) ---')
                    print(f'\tPCM: {MAX_PCM - len(pcm)}/{MAX_PCM} frames disponibles.')
                    return
            else: #La pagina ha sido escrita
                page.m = 0
                page.frec += 1
                page.olr = 0
            #Se mueve la manecilla del reloj a la siguiente pagina
            dram_index = 0 if dram_index + 1 == dramlen else dram_index + 1

# Libera un marco de página de la PCM
def free_frame_pcm():
    global pcm
    global pcm_index

    pcmlen = len(pcm)
    if pcmlen == MAX_PCM : #La pcm ya esta llena
        while(True):
            page = pcm[pcm_index] #La pagina apuntada por la manecilla
            if page.r == 1:
                page.r = 0 #Se cambia su bit R (Segunda oportunidad)
            else:
                #La pagina no ha sido referenciada
                pcm.remove(page) #La manecilla apunta a la siguiente pagina
                if pcm_index == pcmlen : #Se removio la ultima página
                    dram_index = 0 #La manecilla apunta a la primer página
                
                print(f'\t--- Movida a Disco (Proceso {page.owner.pid} Página {page.owner.pageindex(page)}) ---')
                return
            #Se mueve la manecilla del reloj a la siguiente pagina
            pcm_index = 0 if pcm_index + 1 == pcmlen else pcm_index + 1

def updhpt(page_frecuency) :
    global HOT_PAGE_THRESHOLD
    HOT_PAGE_THRESHOLD = (HOT_PAGE_THRESHOLD * (MAX_DRAM - 1) + page_frecuency) / MAX_DRAM