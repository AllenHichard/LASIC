import numpy as np
import skfuzzy as fuzz


class BaseRegras:

    def __init__(self):
        self.t_norma_das_regras = []
        self.valores_linguisticos = {1: "baixo", 2: "medio", 3: "alto"}
        self.regras = []
        self.pesos = []

    def __getRegras__(self):
        return self.regras

    def wangMendel(self, conjuntos_de_entradas_fuzzy, particoes_entradas, instancias):
        for i, instancia in enumerate(instancias):
            atributos = instancia.__getAtributos__()
            classe = instancia.__getClasse__()
            regra = []
            lista_maiores_pertinencias = []
            for conjuntos, particao, valor in zip(conjuntos_de_entradas_fuzzy, particoes_entradas, atributos):
                nivel_baixo = fuzz.interp_membership(particao, conjuntos[0], valor)
                nivel_medio = fuzz.interp_membership(particao, conjuntos[1], valor)
                nivel_alto = fuzz.interp_membership(particao, conjuntos[2], valor)
                pertinencias = [nivel_baixo, nivel_medio, nivel_alto]
                # regra.append(valores_linguisticos[pertinencias.index(max(pertinencias))])
                regra.append(pertinencias.index(max(pertinencias)) + 1)
                lista_maiores_pertinencias.append(max(pertinencias))
            regra.append(classe)
            (cond, index) = self.inconsistencia(self.regras, regra)
            tnorma = np.prod(lista_maiores_pertinencias) # tnorma prod, max, min
            #if tnorma == 0:
                #print(i+1, atributos )
                #print(i+1, lista_maiores_pertinencias)
            if cond and tnorma > 0:
                self.regras.append(regra)
                self.t_norma_das_regras.append(tnorma)
            elif self.t_norma_das_regras[index] < tnorma and tnorma > 0:
                self.regras.__setitem__(index, regra)
                self.t_norma_das_regras.__setitem__(index, tnorma)

        #print(len(self.regras))
        #for regra in self.regras:
            #print(regra)
        #    pass

    def inconsistencia(self, regras, regra):
        for i, r in enumerate(regras):
            if r[:len(r)-1] == regra[:len(regra)-1]:
                #return True, -1
                return False, i  # calcula t norma
        return True, -1

    def calculaPesos(self, conjuntos_de_entradas_fuzzy, particoes_entradas, instancias, outputs):
        for regra in self.regras:
            classificacaoGeral = {}
            for output in outputs:
                classificacaoGeral[outputs[output]] = []
            for instancia in instancias:
                graus_pertinencias = []
                atributos = instancia.__getAtributos__()
                classe = instancia.__getClasse__()
                for i, valor in enumerate(atributos):
                    nível_ativado = regra[i] - 1
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


