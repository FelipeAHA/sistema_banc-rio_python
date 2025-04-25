from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty
from time import sleep
import os

class Cliente:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.__contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.__contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        super().__init__(endereco)
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__cpf = cpf
        self.__senha = senha

    @property
    def nome(self):
        return self.__nome
    
    @property
    def cpf(self):
        return self.__cpf
    
    @property
    def senha(self):
        return self.__senha

class Conta():
    def __init__(self, numero, cliente):
        self.__saldo = 0
        self.__numero = numero
        self.__agencia = '0001'
        self.__cliente = cliente
        self.__historico = Historico()
    
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self.__saldo
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def agencia(self):
        return self.__agencia
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def historico(self):
        return self.__historico
    
    def sacar(self, valor):
        saldo = self.__saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('Saldo insuficiente para realizar a operação.')

        elif valor > 0:
            self.__saldo -= valor
            print(f'Valor sacado com sucesso. Saldo atual: R$ {self.__saldo:.2f}')
            return True
        
        else:
            print('Operação falhou. O valor informado é inválido.')
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f'Valor depositado com sucesso. Saldo atual: R$ {self.__saldo:.2f}')

        else:
            print('Valor inválido para depósito.')
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.__limite = limite
        self.__limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        excedeu_limite = valor > self.__limite
        excedeu_saques = numero_saques >= self.__limite_saques

        if excedeu_limite:
            print('Operação inválida. Valor do saque excede o limite da conta.')

        elif excedeu_saques:
            print('Limite de saques diários atingido. A operação não pode ser realizada.')   
            
        else: 
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'''
        Agência:\t{self.__agencia}
        C/C:\t\t{self.__numero}
        Titular:\t{self.__cliente.nome}
        '''

class Historico():
    def __init__(self):
        self.__transacoes = []
    
    @property
    def transacoes(self):
        return self.__transacoes
    
    def adicionar_transacao(self, transacao):
        self.__transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d/%m/%y %H:%M:%S')
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        ...

    @abstractclassmethod
    def registrar(self, conta):
        ...

class Saque(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor
    
    def registrar (self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def main():
    clientes = []
    contas = []

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

            if clientes:
                for cliente in clientes:
                    if cliente.cpf == cpf:
                        cpf_existente = True
                        break
            
            if cpf_existente:
                print()
                print("Este usuário já existe.")
                limpar_console(menu_inicial)
            else:
                nome = input("Nome do usuário: ")
                data_nascimento = input("Data de nascimento: ")
                lugradouro = input("Informe o lugradouro: ")
                numero = input("Numero: ")
                bairro = input("Bairro: ")
                cidade = input('Cidade: ')
                estado = input('Estado: ')
                senha = input(f"Digite a senha para {nome}: ")
                numero_da_conta = input('Número da conta: ')

                endereco = f'{lugradouro}, nro {numero}, {bairro}, {cidade}, {estado}'

                cliente = PessoaFisica(nome, data_nascimento, cpf, endereco, senha)
                conta = ContaCorrente.nova_conta(numero_da_conta, cliente)
                cliente.adicionar_conta(conta)

                clientes.append(cliente)
                contas.append(conta)

                print()
                print("Usuário criado com sucesso.")
                limpar_console(menu_inicial)
    
    def listar_usuarios():
        print()
        print("~"*30)
        print("Lista de Usuários: ")
        print()
        for cliente in clientes:
            print(cliente.nome.upper())
        print("~"*30)
        voltar(menu_inicial)

    def criar_conta_corrente():

        cpf_titular = input("Digite o CPF do titular da conta: ")

        usuario_existe = False
        conta_existe = False
        cliente_titular = None

        for cliente in clientes:
            if cliente.cpf == cpf_titular:
                usuario_existe = True
                cliente_titular = cliente
                break

        if usuario_existe: 

            numero_da_conta = input('Número da conta: ')

            for conta in contas:
                if conta.numero == numero_da_conta:
                    conta_existe = True
                    break

        else:
            print()
            print("Usuário inexistente. Impossivel criar conta sem usuário.")
            limpar_console(menu_inicial)

        if not conta_existe:
            conta = ContaCorrente.nova_conta(numero_da_conta, cliente_titular)
            cliente_titular.adicionar_conta(conta)
            contas.append(conta)

            print()
            print("Conta criada com sucesso.")
            limpar_console(menu_inicial)
        
        else:
            print('Essa conta já existe.')

    def validar_usuario():
        usuario_login = input("Nome do usuário ou CPF: ")
        senha_usuario = input("Senha do usuário: ")

        cliente_valido = None

        for cliente in clientes:
            if (usuario_login == cliente.nome or usuario_login == cliente.cpf) and senha_usuario == cliente.senha:
                cliente_valido = cliente
                break
        
        if cliente_valido:
            contas_do_cliente = [conta for conta in contas if conta.cliente == cliente_valido]

            if contas_do_cliente:

                conta_escolhida = escolher_conta_usuario(contas_do_cliente)
                conta = contas_do_cliente[conta_escolhida]

                print()
                print("Entrando ...")
                limpar_console(menu_opcoes, conta)

            if not contas_do_cliente:
                print()
                print("Este usuário não possui conta bancária.")
                limpar_console(menu_inicial)

        elif any(usuario_login == cliente.nome or usuario_login == cliente.cpf for cliente in clientes): 
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
            print(f'[{contador}]         {conta.numero}     ---    {conta.saldo}')
            contador += 1
        print('^'*40)
        print()
        while True:
            opcao_usuario = int(input('Escolha a conta que deseja acessar: '))
            if len(lista) >= opcao_usuario > 0:
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

        deposito = Deposito(valor_deposito)
        conta.cliente.realizar_transacao(conta, deposito)

        limpar_console(menu_opcoes, conta)
    
    def sacar(conta):
        valor_saque = float(input('Informe o valor do saque: '))
        print()

        saque = Saque(valor_saque)
        conta.cliente.realizar_transacao(conta, saque)

        limpar_console(menu_opcoes, conta)

    def exibir_extrato(conta):
        if conta.historico.transacoes:
            print("     Data     ---     Valor        ---     Tipo")
            for transacao in conta.historico.transacoes:
                print(f"{transacao['data']}  ---  R$ {transacao['valor']:.2f}     ---  {transacao['tipo']}")
            print()
            print(f"Saldo atual da conta: R$ {conta.saldo:.2f}")
        else: 
            print("Ainda não foram registradas operações nessa conta.")  

        voltar(menu_opcoes, conta)   

    def voltar(func, conta):
        while True:
            print()
            voltar = int(input("Digite [0] para voltar: "))
            if voltar == 0:
                break
            else:
                print("Opção inválida.")
        limpar_console(func, conta)

    def limpar_console(func, conta = None):
        sleep(3)
        os.system("cls" if os.name == "nt" else " clear")  
        if func == menu_inicial:
            menu_inicial()
        else:  
            menu_opcoes(conta)

    def sair():
        print("Encerrando...")
        sleep(3)  

    menu_inicial()

main()    