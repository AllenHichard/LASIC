import LeitorKeel as reader
import LeitorDiretorio as ltr
import teste

paths_treino = ltr.datasets("tra")
for dir in paths_treino:
    obj_reader = reader.LeitorKeel(dir)
    obj_reader.cabecalho()
    #obj_reader.__str__()
    teste.criarConjuntos(obj_reader.inputs)
    teste.criarRegrasWangMendel(obj_reader.data)
    teste.classificar(obj_reader.data)

