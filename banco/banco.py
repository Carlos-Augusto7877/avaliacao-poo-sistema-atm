from .modelos.conta import Conta
from .modelos.cliente import Cliente
from .modelos.operacao import Operacao
from .modelos.conta_corrente import ContaCorrente

class Banco:
    def __init__(self):
        # Banco agrega Contas e Clientes
        self._contas: list[Conta] = []
        self._clientes: list[Cliente] = []
        
    # buscar_conta e buscar_Cliente são funcionalidades genéricas em Banco, usam a mesma lógica de busca.  
    
    def buscar_conta(self, numero) -> Conta:
        for conta in self._contas:
            if conta.numero == numero:
                return conta
            
        return None
    
    def buscar_cliente(self, id):
        for cliente in self._clientes:
            if cliente.id == id:
                return Cliente
        
        return None
    
    
    def transferir(self, origem, destino, valor):
        # valor básico inválido
        if valor <= 0:
            raise ValueError("Valor inválido")

        # não faz sentido transferir pra mesma conta
        if origem is destino:
            raise ValueError("Não é possível transferir para a mesma conta")

        # primeiro tenta sacar da conta de origem
        # aqui já valida saldo + limite automaticamente
        origem.sacar(valor)

        # agora vamos creditar na conta de destino
        if hasattr(destino, "_limite_usado") and destino._limite_usado > 0:
            # se a conta estiver devendo no limite, o dinheiro vai primeiro pra dívida
            if valor <= destino._limite_usado:
                destino._limite_usado -= valor
            else:
                # paga toda a dívida e o resto vira saldo
                sobra = valor - destino._limite_usado
                destino._limite_usado = 0
                destino._saldo += sobra
        else:
            # conta normal ou sem dívida
            destino._saldo += valor

        # por fim, registramos a operação corretamente
        # (uma em cada conta, sem duplicar coisas)
        origem._historico[-1] = Operacao("transferência (saida)", valor)
        destino._historico.append(Operacao("transferência (entrada)", valor))