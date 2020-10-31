import os

caminhoDatasets = os.getcwd()+"/dataset"
def datasets(treino_teste):
    """
        Esse método retorna todos os caminhos dos arquivos que contém os datasets do repositório KEEL
        Caso queira ler arquivos de treino passe como parâmetro datasets("tra")
        Caso queira ler arquivos de teste passe como parâmetro datasets("tst")
        treino_teste:parameter
        datasetsList:return
    """
    datasetsList = []
    for pastaDataset in os.listdir(caminhoDatasets):
        for dataset in os.listdir(caminhoDatasets+"/"+pastaDataset):
            if dataset.__contains__(treino_teste+".dat"):
                datasetsList.append(caminhoDatasets+"/"+pastaDataset+"/"+dataset)
    return datasetsList



