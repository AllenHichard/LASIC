import numpy as np
inicio = 278.0
fim = 1680.0
import decimal
from decimal import Decimal, getcontext

def definirDecimal(fim):
    valor = "0."
    precisao = len(str(fim).split(".")[1])
    for i in range(1, precisao):
        valor+="0"
    valor+="1"
    return float(valor)


if type(fim) == type(0.0):
    n = 100#varia entre 9999 e 10000
    eixo_x = np.arange(inicio, fim, (fim-inicio)/(n - 1))
    eixo_x[len(eixo_x)-1] = fim

    #adicionar no final até completar os pontos
    for i in eixo_x:
        print(i)
        #pass

inicio = 10.6
fim = 30.0
"00"
"0.0001"

if type(fim) == type(0.0):
    #N = 100
    #passo = (fim - inicio)/(N)
    #passo = round(passo, 2)
    print(definirDecimal(fim))
    #getcontext().rounding = decimal.ROUND_DOWN
    print((fim-inicio)/1000)
    eixo_x = np.arange(inicio, fim+definirDecimal(fim), definirDecimal(fim))
    for i in eixo_x:
        #print(i)
        pass

inicio = 0.0
fim = 0.89895
if type(fim) == type(0.0):
    eixo_x = np.arange(inicio, fim+(fim-inicio)/100, (fim-inicio)/100)
    for i in eixo_x:
        #print(i)
        pass

