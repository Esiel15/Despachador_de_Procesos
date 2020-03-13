from enum import Enum

MINPROCESS = 1
MAXPROCESS = 15

MAX_DRAM = 256
MAX_PCM = 512
MAX_VM = 1024

class Process:
    def __init__(self, pid : int, priority : int, refchain : str):
        self.pid = pid
        self.priority = priority
        self.refchain = refchain
        self.waittime = 0
        self.totaltime = 0

        self.genpages()

        self.chain = refchain # Para impresión de resultados

    def genpages(self):
        self.pagelist = []
        maxp = int(self.refchain[0])
        for char in self.refchain:
            if int(char) > maxp:
                maxp = int(char)

        for i in range(maxp):
            self.pagelist.append(Page(owner = self))

    def nextpage(self):
        page, self.refchain = int(self.refchain[0]), self.refchain[1:]
        return self.pagelist[page - 1]

    def show(self):
        print(f'PID: {self.pid}\tPriority: {self.priority}\tReference Chain: {self.refchain}')
    
    def pageindex(self, page):
        return self.pagelist.index(page)

class Page:
    def __init__(self, owner : Process):
        self.r = 0
        self.m = 0
        self.frec = 0
        self.olr = 0
        self.owner = owner
