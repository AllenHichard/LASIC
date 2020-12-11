class Objetivos:

    def __init__(self):
        self.tp_rate = 0
        self.tn_rate = 0
        self.fp_rate = 0
        self.fn_rate = 0
        self.auc = -1
        self.acc = -1
        self.interpretabilidadeCondicoesRegras = 0
        self.interpretabilidadeRegras = 0


    def interpretabilidadeRegra(self, regras, instancias):
        self.interpretabilidadeRegras = (1 - len(regras) / len(instancias))

    def interpretabilidadeCondicoes(self, regras, instancias):
        count = 0
        for r in regras:
            lista = r.antecedentes
            count += len(lista)
            count -= lista.count(-1)
        self.interpretabilidadeCondicoesRegras = (1 - count / len(instancias) * (len(regras[0].antecedentes) + 1))

    def AUC(self, resultado, gabarito):
        if len(resultado) == len(gabarito) and len(resultado) != 0:
            total = len(resultado)
            tn = 0
            tp = 0
            fn = 0
            fp = 0
            for res, gab in zip(resultado, gabarito):
                if res == -1 and gab == -1:
                    tp += 1
                elif res == -2 and gab == -2:
                    tn += 1
                elif res == -1 and gab == -2:
                    fp += 1
                elif res == -2 and gab == -1:
                    fn += 1
            # acurácia
            self.acc = (tn + tp) / total
            # taxa de verdadeiros positivos: é a porcentagem de casos positivos corretamente classificados como pertencentes
            # à classe positiva.
            try:
                self.tp_rate = tp / (tp + fn)
                # taxa de verdadeiros negativos: é a porcentagem de casos negativos corretamente classificados como pertencentes
                # à classe negativa.
                self.tn_rate = tn / (fp + tn)
                # taxa de falsos positivos: é a porcentagem de casos negativos incorretamente classificados como pertencentes
                # à classe positiva.
                self.fp_rate = fp / (fp + tn)
                # taxa de falsos negativos: é a porcentagem de casos positivos incorretamente classificados como pertencentes
                # à classe negativa.
                self.fn_rate = fn / (tp + fn)
            except:
                self.auc = (1 + self.tp_rate - self.fp_rate) / 2


    def ACC(self, resultado, gabarito):
        if len(resultado) == len(gabarito) and len(resultado) != 0:
            total = len(resultado)
            acertou = 0
            for res, gab in zip(resultado, gabarito):
                if res == gab:
                    acertou += 1
            self.acc = acertou / total

