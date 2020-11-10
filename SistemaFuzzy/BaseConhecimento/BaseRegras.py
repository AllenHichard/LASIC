import numpy as np
import skfuzzy as fuzz


class BaseRegras:

    def __init__(self):
        self.t_norma_das_regras = []
        self.valores_linguisticos = {1: "baixo", 2: "medio", 3: "alto"}
        self.regras = [[], []] # antecedentes, consequentes
        self.pesos = []

    def __getRegras__(self):
        return self.regras

    def wangMendel(self, conjuntos_de_entradas_fuzzy, particoes_entradas, instancias):
        for i, instancia in enumerate(instancias):
            atributos = instancia.__getAtributos__()
            classe = instancia.__getClasse__()
            antecedentes = [] #antiga regra
            lista_maiores_pertinencias = []
            for conjuntos, particao, valor in zip(conjuntos_de_entradas_fuzzy, particoes_entradas, atributos):
                nivel_baixo = fuzz.interp_membership(particao, conjuntos[0], valor)
                nivel_medio = fuzz.interp_membership(particao, conjuntos[1], valor)
                nivel_alto = fuzz.interp_membership(particao, conjuntos[2], valor)
                pertinencias = [nivel_baixo, nivel_medio, nivel_alto]
                # regra.append(valores_linguisticos[pertinencias.index(max(pertinencias))])
                antecedentes.append(pertinencias.index(max(pertinencias)) + 1)
                lista_maiores_pertinencias.append(max(pertinencias))
            #regra.append(classe)
            (cond, index) = self.inconsistencia(self.regras, antecedentes)
            tnorma = np.prod(lista_maiores_pertinencias) # tnorma prod, max, min
            #if tnorma == 0:
                #print(i+1, atributos )
                #print(i+1, lista_maiores_pertinencias)
            if cond and tnorma > 0:
                self.regras[0].append(antecedentes)
                self.regras[1].append(classe)
                self.t_norma_das_regras.append(tnorma)
            elif self.t_norma_das_regras[index] < tnorma and tnorma > 0:
                self.regras[0].__setitem__(index, antecedentes)
                self.regras[1].__setitem__(index, classe)
                self.t_norma_das_regras.__setitem__(index, tnorma)

        #print(len(self.regras))
        #for regra in self.regras:
            #print(regra)
        #    pass

    def inconsistencia(self, regras, antecedentes):
        for i, r_ant in enumerate(regras[0]): # lista de antecedentes das regras
            if r_ant == antecedentes:
                #return True, -1
                return False, i  # calcula t norma
        return True, -1

    def calculaPesos(self, conjuntos_de_entradas_fuzzy, particoes_entradas, instancias, outputs):
        for antecedentes in self.regras[0]:
            classificacaoGeral = {}
            for output in outputs:
                classificacaoGeral[outputs[output]] = []
            for instancia in instancias:
                graus_pertinencias = []
                atributos = instancia.__getAtributos__()
                classe = instancia.__getClasse__()
                for i, valor in enumerate(atributos):
                    nível_ativado = antecedentes[i] - 1
                    grau = fuzz.interp_membership(particoes_entradas[i],
                                                  conjuntos_de_entradas_fuzzy[i][nível_ativado],
                                                  valor)
                    graus_pertinencias.append(grau)
                compatibilidade = np.prod(graus_pertinencias)  # operador produto #u1*u2*.....*un
                classificacaoGeral[classe].append(compatibilidade)
            lista_bg = []
            for classe in classificacaoGeral:
                bg = np.sum(classificacaoGeral[classe])
                lista_bg.append(bg)
            Bgx = np.max(lista_bg)
            M = len(lista_bg)
            lista_bg.remove(Bgx)
            betha = np.sum(lista_bg) / (M-1)
            numerador = abs(Bgx - betha)
            denonimador = np.sum(lista_bg) + Bgx
            CF = numerador/denonimador
            self.pesos.append(CF)
        #print(len(self.regras), len(self.pesos))
        #print(self.pesos)
        return self.pesos


