class Objetivos:

    def __init__(self):
        self.tp_rate = 0
        self.tn_rate = 0
        self.fp_rate = 0
        self.fn_rate = 0
        self.auc = 0

    def __getTaxaVerdadeiroPositivo__(self):
        return self.tp_rate

    def __getTaxaVerdadeiroNegativoPositivo__(self):
        return self.tn_rate

    def __getTaxaFalsoPositivo__(self):
        return self.fp_rate

    def __getTaxaFalsoNegativo__(self):
        return self.fn_rate

    def __getAcuraciaDatasetDesbalanceado__(self, resultado, gabarito):
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
            acc = (tn + tp) / total
            # taxa de verdadeiros positivos: é a porcentagem de casos positivos corretamente classificados como pertencentes
            # à classe positiva.
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
            self.auc = (1 + self.tp_rate - self.fp_rate) / 2
            return acc
        else:
            return -1

    def __getAUC__(self):
        return self.auc

    def __getAcuraciaDatasetBalanceado__(self, resultado, gabarito):
        if len(resultado) == len(gabarito) and len(resultado) != 0:
            total = len(resultado)
            acertou = 0
            for res, gab in zip(resultado, gabarito):
                if res == gab:
                    acertou += 1
            acc = acertou / total
            return acc
        else:
            return -1