from modelos import Conta, Cliente
from datetime import datetime

class Operacao:
    def __init__(self, tipo, cliente: Cliente, conta: Conta):
        self.tipo = tipo
        self.cliente = cliente
        self.conta = conta
        self.data = datetime.now()