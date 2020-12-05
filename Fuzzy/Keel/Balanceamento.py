from collections import Counter

class Balanceamento:
    def __init__(self):
        self.classes = []

    def __addClasse__(self, classe):
        self.classes.append(classe)

    def __getBalanceamento__(self):
        print(dict(Counter(self.classes)))
