from modelos import Conta

class Cliente:
    def __init__(self, nome, numero):
        self.nome = nome
        self.numero = numero
        self._contas = [Conta]