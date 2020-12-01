from ExtracaoKeel import LeitorDiretorio as ltr
from Config import ParametrosJSON as json
import SBRF
import AGMO
inputs = json.getArcEntrada()
fuzzy, ag = inputs['SISTEMA']
conjuntos = inputs['CONJUNTO_FUZZY']
granularidade = inputs['GRANULARIDADE']
composicao = inputs['OPERADOR_COMPOSICAO']
agregacao = inputs['OPERADOR_AGREGACAO']
inferencia = inputs['INFERENCIA']
temPeso = inputs['PESOS']
default = inputs['DEFAULT']

paths_treino = ltr.datasets("tra")
paths_teste = ltr.datasets("tst")

if fuzzy:
    print("Execução do Sistema Fuzzy")
    SBRF.SistemaFuzzy(paths_treino, paths_teste, agregacao,composicao, temPeso)
if ag:
    print("Execução do Algoritmo Genético")
    AGMO.algoritmoGenetico(paths_treino, paths_teste, agregacao,composicao, temPeso)