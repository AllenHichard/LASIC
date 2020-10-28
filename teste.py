import numpy as np
inicio = 278.0
fim = 1680.0
if type(fim) == type(0.0):
    eixo_x = np.arange(inicio, fim+(inicio/fim), inicio/fim)
    #eixo_x = np.arange(inicio, fim + (fim - inicio) / 1000, (fim - inicio) / 1000)
    for i in eixo_x:
        print(i)
        pass

inicio = 10.6
fim = 30.0
if type(fim) == type(0.0):
    #eixo_x = np.arange(inicio, fim+(fim-inicio)/1000, (fim-inicio)/1000)
    for i in eixo_x:
        #print(i)
        pass
inicio = 0.0
fim = 0.89
if type(fim) == type(0.0):
    eixo_x = np.arange(inicio, fim+(fim-inicio)/100, (fim-inicio)/100)
    for i in eixo_x:
        print(i)
        pass

