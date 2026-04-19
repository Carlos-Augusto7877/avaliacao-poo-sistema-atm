from modelos import Cliente, Operacao

class Conta:
    def __init__(self, cliente: Cliente, numero):
        self.cliente = cliente
        self.numero = numero
        self._saldo = 0
        self._historico = [Operacao("criacao", self, self.cliente)]
        self.cliente._contas.append(self)
    
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido")
    
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        
        self._saldo -= valor
        self._historico.append(Operacao("saque", self, self.cliente))
        
    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido")
        
        self._saldo += valor
        self._historico.append(Operacao("deposito", self, self.cliente))
        
    def mostrar_historico(self):
        if self._historico == []:
            print("Histórico vazio. Não há operações registradas nessa conta.")
        else:
            for op in self._historico:
                print(op)
            