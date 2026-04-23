import time
from banco import Banco
from banco.modelos.conta import Conta
from banco.modelos.cliente import Cliente
from banco.modelos.conta_corrente import ContaCorrente
from banco.modelos.conta_poupanca import ContaPoupanca

LIMITE = 500

# instância única do sistema (simples, sem complicar)
banco = Banco()


def criar_cliente():
    print("\n--- Cadastro de cliente ---")

    nome = input("Nome: ")
    cliente = Cliente(nome)

    banco._clientes.append(cliente)
    print("Cliente criado com sucesso!")
    return cliente


def criar_conta(cliente: Cliente):
    print("\n--- Criar conta ---")

    tipo = input("Tipo (1 - Normal | 2 - Corrente | 3 - Poupança): ")

    if tipo == "1":
        conta = Conta(cliente)
    elif tipo == "2":
        conta = ContaCorrente(cliente, LIMITE)
    elif tipo == "3":
        conta = ContaPoupanca(cliente)
    else:
        print("Tipo inválido.")
        return

    banco._contas.append(conta)
    print("Conta criada com sucesso!")
    if isinstance(conta, ContaCorrente):
        print(f"Seu limite é {LIMITE}")
    return conta


def listar_contas(cliente: Cliente):
    print("\n--- Contas ---")
    if cliente._contas == []:
        print("Voce ainda não tem contas nesse banco.")
    else:
        for i, conta in enumerate(cliente._contas):
            if isinstance(conta, ContaCorrente):
                tipo = "corrente"
            elif isinstance(conta, ContaPoupanca):
                tipo = "poupança"
            else:
                tipo = "padrão"
            print(f"[{i + 1}] Tipo: {tipo} | Numero: {conta.numero} | Saldo: R${conta._saldo:.2f}")
            
    print("--------------\n")


def sacar(conta: Conta):
    print("\n--- Saque ---")

    if not conta:
        return

    try:
        valor = float(input("Valor: "))
        conta.sacar(valor)
        print("Saque realizado.")
    except Exception as e:
        print(f"Erro: {e}")


def depositar(conta: Conta):
    print("\n--- Depósito ---")

    if not conta:
        return

    try:
        valor = float(input("Valor: "))
        conta.depositar(valor)
        print("Depósito realizado.")
    except Exception as e:
        print(f"Erro: {e}")


def transferir(conta: Conta):
    print("\n--- Transferência ---")

    print("Conta de origem:")
    origem = conta
    if not origem:
        return

    destino = None
    num_destino = int(input("Conta de destino (digite o numero):"))
    
    for conta in banco._contas:
        if conta.numero == num_destino:
            destino = conta
    
    if not destino:
        return

    try:
        valor = float(input("Valor: "))
        banco.transferir(origem, destino, valor)
        print("Transferência realizada.")
    except Exception as e:
        print(f"Erro: {e}")


def mostrar_historico(conta: Conta):
    print("\n--- Histórico ---")

    conta.mostrar_historico()

def verificar_limite(conta: ContaCorrente):
    limite = conta.limite
    limite_disponivel = limite - conta._limite_usado
    print(f"seu limmite é R${limite:.2f}. E ainda tem disponível R${limite_disponivel:.2f}")

def menu_principal():
    while True:
        print("\n===== MENU INICIAL =====")
        print("1 - Cadastrar cliente")
        print("2 - Entrar como cliente")
        print("0 - Sair")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                cliente = criar_cliente()
                menu_cliente(cliente)

            case "2":
                cliente = None
                idx = int(input("Informe o id: "))
                for cli in banco._clientes:
                    if cli.id == idx:
                        cliente = cli

                menu_cliente(cliente)

            case "0":
                print("Saindo...")
                break

            case _:
                print("Opção inválida.")

        print("------------------")

def menu_cliente(cliente: Cliente):
    print(f"\n===== Cliente: {cliente.nome}")
    
    while True:
        print("1 - Criar Conta")
        print("2 - Entrar em conta existente (iniciar sessão)")
        print("3 - Sair")
        opcao = int(input("Escolha uma opção: "))
        
        match opcao:
            case 1:
                conta = criar_conta(cliente)
                menu_conta(conta)
            case 2:
                print("----- Contas cadastradas -----")
                while True:
                    listar_contas(cliente)
                    if len(cliente._contas) == 0:
                        break
                    opcao = int(input("Selecione uma conta: "))
                    if opcao > len(cliente._contas) or opcao < 1:
                        print(f"Opção inválida escolha uma das contas a partir de seu número na lista de 1 a {len(cliente._contas)}")
                    else:
                        conta = cliente._contas[opcao - 1]
                        menu_conta(conta)
                        break

            case 3:
                print("saindo do mennu de cliente...")
                time.sleep(1.0)
                break
                
            case _:
                print("Opção inválida")
                
        
        print("------------------")
            
    
def menu_conta(conta: Conta):
    while True:
        time.sleep(1.0)
        print("\n===== MENU DA CONTA =====")
        print("1 - Sacar")
        print("2 - Depositar")
        print("3 - Transferir")
        print("4 - Mostrar histórico")
        print("5 - informações sobre a conta")

        # só aparece se for conta corrente
        if isinstance(conta, ContaCorrente):
            print("6 - Aumentar limite")
            print("7 - Voltar")
            print("0 - Sair")
        else:
            print("6 - Voltar")
            print("0 - Sair")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                sacar(conta)
            case "2":
                depositar(conta)

            case "3":
                transferir(conta)

            case "4":
                conta.mostrar_historico()
            
            case "5":
                time.sleep(1.0)
                print(f"Saldo: R${conta._saldo:.2f}")
                print(f"Número de operações: {len(conta._historico)}")
                
                if isinstance(conta, ContaCorrente):
                    verificar_limite(conta)

            case "6":
                if isinstance(conta, ContaCorrente):
                    try:
                        conta.aumentar_limite()
                        print("Limite atualizado.")
                    except Exception as e:
                        print(f"Erro: {e}")
                else:
                    print("Saindo da sessão de conta atual...")
                    time.sleep(1.0)
                    return  # voltar

            case "7":
                if isinstance(conta, ContaCorrente):
                    print("Saindo da sessão de conta atual...")
                    time.sleep(1.0)
                    return  # voltar

            case "0":
                print("Saindo...")
                exit()

            case _:
                print("Opção inválida.")
                
        
        print("------------------")


if __name__ == "__main__":
    menu_principal()