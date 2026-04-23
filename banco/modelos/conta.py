from .operacao import Operacao

class Conta:
    _numero_counter = 0
    
    def __init__(self, cliente):
        # dados comuns de uma conta ao ser incializada
        self.cliente = cliente
        self._saldo = 0
        self.numero = Conta._numero_counter # lógica de autoincrementação em classes
        Conta._numero_counter += 1
        self._historico: list[Operacao ]= [] # historico guarda todas as operações realizadas em uma conta
        self.cliente._contas.append(self) # agregação imediata de conta ao Cliente que a possui
    
    def sacar(self, valor):
        # validações de entrada
        if valor <= 0:
            raise ValueError("Valor inválido")
    
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente")
        
        self._saldo -= valor
        self._historico.append(Operacao("saque", valor)) # operação já é registrada
        
        
    def depositar(self, valor):
        # validações de entrada
        if valor <= 0:
            raise ValueError("Valor inválido")
        
        self._saldo += valor
        self._historico.append(Operacao("deposito", valor)) # registro imediato da operação
        
    def mostrar_historico(self):
        # método que permite visualizar o historico da conta, ou seja todas as operações, a partir da iteração.
        if self._historico == []:
            print("Histórico vazio. Não há operações registradas nessa conta.")
        else:
            for op in self._historico:
                op.mostrar_operacao()
    
    def aumentar_limite(self):
        # somente conta corrente possui limite
        raise NotImplementedError("Conta não suporta limite, funcionaiidade exclusiva para conta corrente.")