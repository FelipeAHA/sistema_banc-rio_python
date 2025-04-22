from datetime import date
from time import sleep
import os

numero_da_conta = " "
titular = " "
saldo = 0
numero_agencia = " "
extrato = []
quantidade_saques_por_dia = 1
LIMITE_QUANTIDADE_SAQUES = 3
limite_valor_saques = 500

dia_atual = date.today()

def menu():
    print("="*20)
    print("""
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair
          """)
    print("="*20)
    print()
    opcao_usuario = int(input("Escolha uma opção: "))
    print()

    if opcao_usuario == 1:
        depositar()
    elif opcao_usuario == 2:
        sacar()
    elif opcao_usuario == 3:
        exibir_extrato()
    elif opcao_usuario == 4:
        sair()
    else:
        print("Opção inválida. Escolha uma das opções disponíveis.")    
        limpar_console()


def depositar():
    valor_deposito = float(input("Informe o valor do depósito: "))
    print()
    global saldo 
    if valor_deposito > 0:
        saldo += valor_deposito
        transacao = (valor_deposito, date.today(), "DEPÓSITO")
        extrato.append(transacao)
        print(f"Valor depositado com sucesso. Saldo atual: R$ {saldo:.2f}")
        limpar_console()
    else:
        print("Valor inválido para depósito.")
        limpar_console()

def sacar():
    valor_saque = float(input("Informe o valor do saque: "))
    print()

    global dia_atual
    global quantidade_saques_por_dia
    global saldo

    if valor_saque <= saldo and limite_valor_saques >= valor_saque > 0 and quantidade_saques_por_dia <= LIMITE_QUANTIDADE_SAQUES:
            
            saldo -= valor_saque
            transacao = (-valor_saque, date.today(), "SAQUE")
            extrato.append(transacao)

            if dia_atual == date.today():
                quantidade_saques_por_dia += 1
            else:
                quantidade_saques_por_dia = 0 
                dia_atual = date.today()    

            print(f"Valor sacado com sucesso. Saldo atual: R$ {saldo:.2f}")
            limpar_console()

    else:
        mensagem = " "
        if valor_saque > saldo: 
            mensagem = "Saldo insufciciente para esta operação."
        elif quantidade_saques_por_dia > 3:
            mensagem = "Limite de saques diários atingido. A operação não pode ser realizada."
        else: 
            mensagem = "Valor inválido para saque."
        print(mensagem)
        limpar_console()

def exibir_extrato():
    if extrato:
        print("Data     ---     Valor     ---     Status")
        for transacao in extrato:
            print(f"{transacao[1]}  ---  R$ {transacao[0]:.2f}  ---  {transacao[2]}")
        print()
        print(f"Saldo atual da conta: R$ {saldo:.2f}")
    else: 
        print("Ainda não foram registradas operações no extrato.")        

    while True:
        print()
        voltar = int(input("Digite [0] para voltar: "))
        if voltar == 0:
            break
        else:
            print("Opção inválida.")
    limpar_console()

def sair():
    print("Encerrando...")
    sleep(3)

def limpar_console():
    sleep(3)
    os.system("cls" if os.name == "nt" else " clear")    
    menu()

menu()
        
        
        



