from .conta import Conta

class ContaPoupanca(Conta):
    def __init__(self, cliente):
        super().__init__(cliente)