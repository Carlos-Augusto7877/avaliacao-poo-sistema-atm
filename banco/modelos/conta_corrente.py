from .conta import Conta
from .operacao import Operacao

class ContaCorrente(Conta):
    def __init__(self, cliente, limite=0):
        super().__init__(cliente)
        # Conta corrente se diferencia pelo uso de limite ou cheque especial, que concede uma valor adicional a ser sacado dependendo da conta
        self.limite = limite
        self._limite_usado = 0
        
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido")

        if valor > self._saldo + (self.limite - self._limite_usado):
            raise ValueError("Saldo insuficiente")

        if valor <= self._saldo:
            self._saldo -= valor
        else:
            restante = valor - self._saldo
            self._saldo = 0
            self._limite_usado += restante

        self._historico.append(Operacao("saque", valor))
    
    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido")

        if self._limite_usado > 0:
            if valor <= self._limite_usado:
                # paga só a dívida
                self._limite_usado -= valor
                self._historico.append(Operacao("pagamento de limite", valor))
            else:
                # paga toda a dívida e sobra dinheiro
                sobra = valor - self._limite_usado

                self._historico.append(
                    Operacao("pagamento de limite", self._limite_usado)
                )

                self._limite_usado = 0

                # agora o resto vira saldo normal
                super().depositar(sobra)
        else:
                super().depositar(valor)
        
    def aumentar_limite(self):
        # cálculo do novo limite usando dados já disponíveis em conta
        # dados relevantes: número de operações & maior valor movimentado
        if self._limite_usado > 0:
            raise ValueError(f"Não foi possível aumentar o limite, a conta precisa primeiramente pagar a dívida atual: R${self._limite_usado:.2f}")
        
        num_ops = len(self._historico)
        maior_valor = max((op.valor or 0 for op in self._historico), default=0)
        
        self.limite += (num_ops * 10) + (0.1*maior_valor)
        
        