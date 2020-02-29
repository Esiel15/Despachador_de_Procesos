import sys
import argparse
from random import randint

MIN_LEN_REFCHAIN = 5

def main() :
    # Inicialización
    p, r, k, filename = init()
    file = open(filename, 'w')
    for i in range(p):
        priority = randint(1, r) #r-prioridad
        pmax = randint(1, 9) #Paginas diferentes por proceso
        output = str(i+1) + ',' + str(priority) + ',' #<Process ID>,<priority>,

        for j in range(randint(MIN_LEN_REFCHAIN, k)): #k-numero de paginas por proceso
            output += str(randint(1, pmax))
        file.write(output + '\n')
    file.close()

# Inicialización del programa
def init():
    # Verifica los argumentos de la ejecución
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        nargs = 1,
                        type = int,
                        default = 200,
                        help = '<Número de procesos> (Por defecto: 200)')
    parser.add_argument('-r',
                        nargs = 1,
                        type = int,
                        default = 5,
                        help = '<Prioridad máxima por proceso> (Por defecto: 5)')                   
    parser.add_argument('-k',
                        nargs = 1,
                        type = int,
                        default = 200,
                        help = '<Longitud de la cadena de referencia por proceso> (Por defecto: 200)')
    parser.add_argument('-f',
                        nargs = 1,
                        type = str,
                        default = 'input.txt',
                        help = '<nombre del archivo> (Por defecto: "input.txt")')
    args = parser.parse_args()

    if args.p[0] < 1:
        print('Se debe generar al menos 1 proceso.\n')
        exit()
    if args.r[0] < 5:
        print('Los procesos no pueden tener una prioridad menor a 5.\n')
        exit()
    if args.k[0] < 1:
        print('La longitud de la cadena de referencia debe ser al menos 1.\n')
        exit()
    return args.p[0], args.r[0], args.k[0], args.f
# Fin init


if __name__ == '__main__':
    main()