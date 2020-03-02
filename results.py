import common

def output(finished, aniquilated, systime, refcount, pfcount):
    r = open('results.txt', 'w', encoding="utf-8")
    r.write('Resultados de la Simulación\n\n')
    r.write(f'Tiempo total: {round(systime, 4)}\n')
    r.write(f'Total de Referencias hechas: {refcount}\n')
    r.write(f'Total de Fallos de Página: {pfcount}\n')
    r.write('Tamaño de las memorias:\n')
    r.write(f'DRAM: {common.MAX_DRAM} marcos.\n')
    r.write(f'PCM: {common.MAX_PCM} marcos.\n')
    r.write(f'Memoria Virtual: {common.MAX_VM} marcos.\n')
    r.write('\n\t|| Procesos Ejecutados ||\n')
    
    r.write('PID\tPrior.\tT. Total\tT. Espera\tCadena de Referencia\n')
    for fproc in finished:
        r.write(f'{fproc.pid}\t{fproc.priority}\t\t{fproc.totaltime}\t\t\t{fproc.waittime}\t\t\t{fproc.chain}\n')

    r.write('\n\t|| Procesos Aniquilados ||\n')
    
    r.write('PID\tPrior.\tCadena de Referencia\n')
    for aproc in aniquilated:
        r.write(f'{aproc.pid}\t{aproc.priority}\t\t\t{aproc.chain}\n')


    o = open('output.csv', 'w')
    o.write('PID,Prioridad,Tiempo Total,Tiempo de Espera,Cadena de Referencia\n')
    for fproc in finished:
        o.write(f'{fproc.pid},{fproc.priority},{fproc.totaltime},{fproc.waittime},{fproc.chain}\n')

    o.write('\nPID,Prioridad,Cadena de Referencia\n')
    for aproc in aniquilated:
        o.write(f'{aproc.pid},{aproc.priority},{aproc.chain}\n')

    o.write('Total Ref,Total Page Fault,Total System Time,DRAM Frames,PCM Frames,VM Frames\n')
    o.write(f'{refcount},{pfcount},{systime},{common.MAX_DRAM},{common.MAX_PCM},{common.MAX_VM}')

