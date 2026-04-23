from datetime import datetime

class Operacao:
    def __init__(self, tipo: str, valor):
        agora = datetime.now()
        formatado = agora.strftime("%d/%m/%Y %H:%M")
        self.tipo = tipo
        self.valor = valor
        self._data = formatado # data da operação efetuada
        
    def mostrar_operacao(self):
        print(f"Tipo: {self.tipo}\nValor: R${self.valor:.2f}\nData: {self._data}\n")