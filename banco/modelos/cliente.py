from .conta import Conta

class Cliente:
    _id_counter = 0 # variável da classe
    
    def __init__(self, nome):
        # dados comuns ao incializar Cliente
        self.nome = nome
        self.id = Cliente._id_counter
        Cliente._id_counter += 1 # lógica de autoincrementação na classe
        self._contas: list[Conta] = [] 
        
    @property
    def saldo_total(self):
        # função que retorna o saldo total do cliente somando o saldo de todas as suas contas, método transoformado em property para melhor praticidde
        stot = 0
        for acc in self._contas:
            stot += acc._saldo
            
        return stot