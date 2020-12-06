import numpy as np
import skfuzzy as fuzz
from ClassificadorFuzzy.Model import Regra
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.BaseDados import BaseDados as bd
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.AlgoritmoRegras.WangMendel import WangMendel
from ClassificadorFuzzy.SistemaFuzzy.BaseConhecimento.AlgoritmoRegras.Aleatorio import Aleatorio


class BaseRegras:
    def __init__(self, particoes, instancias, classes):
        self.particoes = particoes
        self.instancias = instancias
        self.classes = classes

    def getRegras(self, metodo=""):
        if str(metodo).__eq__("Wang-Mendel"):
            wm = WangMendel(self.particoes, self.instancias)
            return wm.wangMendel()
        else:
            aleatorio = Aleatorio(self.particoes, self.instancias, self.classes)
            return aleatorio.aleatorio()






"""
mudou a entrada para instâncias
BaseDados = bd.BaseDados([0,100], [100, 200], [1000,1000], [["TRAP", "TRI", "TRAP"],["TRAP", "TRI", "TRAP"]])
particoes = BaseDados.criarParticoes()
entradas = [[0,140],[0,168], [0,189]]
saidas = [1,2,1]
br = BaseRegras(particoes, entradas, saidas)
br.wangMendel()
print("BaseRegras")
br.printRegras()
"""