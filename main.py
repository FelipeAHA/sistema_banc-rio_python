from datetime import date
from time import sleep
import os


lista_de_usuarios = []
lista_de_contas_corrente = []
numero_da_conta = 1
numero_agencia = '0001'


def menu_inicial():
    print("="*40)
    print("""
    [1] Criar usuário
    [2] Listar usuários
    [3] Criar conta corrente
    [4] Entrar com usuário existente
    [5] Sair
          """)
    print("="*40)
    print()
    opcao_usuario = int(input("Escolha uma opção: "))
    print()

    if opcao_usuario == 1:
        criar_usuario()
    elif opcao_usuario == 2:
        listar_usuarios()
    elif opcao_usuario == 3:
        criar_conta_corrente()
    elif opcao_usuario == 4:
        validar_usuario()
    elif opcao_usuario == 5:
        sair()
    else:
        print("Opção inválida. Escolha uma das opções disponíveis.")    
        limpar_console(menu_inicial)

def criar_usuario():

    cpf = input("Informe o CPF (somente números): ")
    
    cpf_existente = False

    for usuario in lista_de_usuarios:
        if cpf == usuario[0]:
            cpf_existente = True
            break
    
    if cpf_existente:
        print()
        print("Este usuário já existe.")
        limpar_console(menu_inicial)
    else:
        nome_usuario = input("Nome do usuário: ")
        data_nascimento = input("Data de nascimento: ")
        lugradouro = input("Informe o lugradouro: ")
        numero = input("Numero: ")
        bairro = input("Bairro: ")
        cidade = input('Cidade: ')
        estado = input('Estado: ')
        senha_usuario = input(f"Digite a senha para {nome_usuario}: ")

        endereco = f'{lugradouro}, nro {numero}, {bairro}, {cidade}, {estado}'

        usuario = {'cpf': cpf, 'nome_usuario': nome_usuario, 'data_nascimento': data_nascimento, 'endereço': endereco, 'senha': senha_usuario}
        lista_de_usuarios.append(usuario)
        print()
        print("Usuário criado com sucesso.")
        limpar_console(menu_inicial)


def listar_usuarios():
    print()
    print("~"*30)
    print("Lista de Usuários: ")
    print()
    for usuario in lista_de_usuarios:
        print(usuario['nome_usuario'])
    print("~"*30)
    voltar(menu_inicial)

def criar_conta_corrente():

    titular = input("Digite o usuário titular da conta: ")

    usuario_existe = False
    conta_existe = False

    for usuario in lista_de_usuarios:
        if titular == usuario['nome_usuario']:
            usuario_existe = True
            break

    if usuario_existe: 

        global numero_da_conta, numero_agencia

        conta = {'titular': titular, "numero_da_conta": numero_da_conta, "numero_agencia": numero_agencia, "saldo": 0, "extrato": [], "limite_valor_saque": 500, "limite_quantidade_saques": 3, "quantidade_saques_por_dia": 1, "dia_atual": date.today()}
        lista_de_contas_corrente.append(conta)
        numero_da_conta += 1
        print()
        print("Conta criada com sucesso.")
        limpar_console(menu_inicial)
    else:
        print()
        print("Usuário inexistente. Impossivel criar conta sem usuário.")
        limpar_console(menu_inicial)


def validar_usuario():
    usuario_login = input("Nome do usuário ou CPF: ")
    senha_usuario = input("Senha do usuário: ")

    usuario_valido = None

    for usuario in lista_de_usuarios:
        if (usuario_login == usuario['nome_usuario'] or usuario_login == usuario['cpf']) and senha_usuario == usuario['senha']:
            usuario_valido = usuario
            break
    
    if usuario_valido:
        lista_de_contas_do_usuario = [conta for conta in lista_de_contas_corrente if conta['titular'] == usuario_valido['nome_usuario']]

        if lista_de_contas_do_usuario:

            conta_escolhida = escolher_conta_usuario(lista_de_contas_do_usuario)
            conta = lista_de_contas_do_usuario[conta_escolhida]

            print()
            print("Entrando ...")
            limpar_console(menu_opcoes, conta)

        if not lista_de_contas_do_usuario:
            print()
            print("Este usuário não possui conta bancária.")
            limpar_console(menu_inicial)

    elif any(usuario_login == usuario['nome_usuario'] or usuario_login == usuario['cpf'] for usuario in lista_de_usuarios): 
            print()
            print("Senha incorreta.")
            limpar_console(menu_inicial)
    else:
        print()
        print("Usuário inexistente.")    
        limpar_console(menu_inicial)
    

def escolher_conta_usuario(lista):
    print('^'*40)
    print('     Número da conta  ---  Saldo')
    contador = 1
    for conta in lista:
        print(f'[{contador}]         {conta['numero_da_conta']}     ---    {conta['saldo']}')
        contador += 1
    print('^'*40)
    print()
    while True:
        opcao_usuario = int(input('Escolha a conta que deseja acessar: '))
        if len(lista) >= opcao_usuario >= 0:
            break
        else:
            print()
            print('Opção invalida. Escolha uma das contas disponíveis.')
    return opcao_usuario - 1


def menu_opcoes(conta):
    print("="*40)
    print("""
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Voltar ao menu inicial
    [5] Sair
          """)
    print("="*40)
    print()
    opcao_usuario = int(input("Escolha uma opção: "))
    print()

    if opcao_usuario == 1:
        depositar(conta)
    elif opcao_usuario == 2:
        sacar(conta)
    elif opcao_usuario == 3:
        exibir_extrato(conta)
    elif opcao_usuario == 4:
        limpar_console(menu_inicial)
    elif opcao_usuario == 5:
        sair()
    else:
        print("Opção inválida. Escolha uma das opções disponíveis.")    
        limpar_console(menu_opcoes, conta)


def depositar(conta):
    valor_deposito = float(input("Informe o valor do depósito: "))
    print()

    if valor_deposito > 0:
        conta['saldo'] += valor_deposito
        transacao = (valor_deposito, date.today(), "DEPÓSITO")
        conta['extrato'].append(transacao)
        print(f"Valor depositado com sucesso. Saldo atual: R$ {conta['saldo']:.2f}")
        limpar_console(menu_opcoes, conta)
    else:
        print("Valor inválido para depósito.")
        limpar_console(menu_opcoes, conta)

def sacar(conta):
    valor_saque = float(input("Informe o valor do saque: "))
    print()

    if valor_saque <= conta['saldo'] and conta['limite_valor_saque'] >= valor_saque > 0 and conta['quantidade_saques_por_dia'] <= conta['limite_quantidade_saques']:
            
            conta['saldo'] -= valor_saque
            transacao = (-valor_saque, date.today(), "SAQUE")
            conta['extrato'].append(transacao)

            if conta["dia_atual"] == date.today():
                conta["quantidade_saques_por_dia"] += 1
            else:
                conta["quantidade_saques_por_dia"] = 1 
                conta["dia_atual"] = date.today()    

            print(f"Valor sacado com sucesso. Saldo atual: R$ {conta['saldo']:.2f}")
            limpar_console(menu_opcoes, conta)

    else:
        mensagem = " "
        if valor_saque > conta['saldo']: 
            mensagem = "Saldo insufciciente para esta operação."
        elif conta["quantidade_saques_por_dia"] > 3:
            mensagem = "Limite de saques diários atingido. A operação não pode ser realizada."
        else: 
            mensagem = "Valor inválido para saque."
        print(mensagem)
        limpar_console(menu_opcoes, conta)

def exibir_extrato(conta):
    if conta["extrato"]:
        print("Data     ---     Valor     ---     Status")
        for transacao in conta["extrato"]:
            print(f"{transacao[1]}  ---  R$ {transacao[0]:.2f}  ---  {transacao[2]}")
        print()
        print(f"Saldo atual da conta: R$ {conta['saldo']:.2f}")
    else: 
        print("Ainda não foram registradas operações nessa conta.")  

    voltar(menu_opcoes, conta)      

def voltar(func, conta=None):
    while True:
        print()
        voltar = int(input("Digite [0] para voltar: "))
        if voltar == 0:
            break
        else:
            print("Opção inválida.")
    limpar_console(func, conta)

def sair():
    print("Encerrando...")
    sleep(3)

def limpar_console(func, conta = None):
    sleep(3)
    os.system("cls" if os.name == "nt" else " clear")  
    if func == menu_inicial:
        menu_inicial()
    else:  
        menu_opcoes(conta)

menu_inicial()
