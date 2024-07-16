from abc import ABC, abstractmethod
import re


# ======================================================  Inicio Cliente  ======================================================#
usuarios = []

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    @classmethod
    def novo_cliente(cls, endereco):
        return cls(endereco)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
        
    @property
    def nome(self):
        return self._nome
        
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    @classmethod
    def novo_cliente(cls, cpf, nome, data_nascimento, endereco):
        return cls(cpf, nome, data_nascimento, endereco)

# ========================================================  Fim Cliente  =======================================================#

# =======================================================  Inicio Classe Conta  =======================================================#
todas_contas = []

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._hitorico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo += valor

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._hitorico
    
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

class ContaCorrente(Conta):
    def __init__(self,numero, cliente, limite = 500., limite_saques = 3):
        super().__init__(numero, cliente)
        self._numero_saques = 0
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def numero_saques(self):
        return self._numero_saques
    
    @numero_saques.setter
    def numero_saques (self, valor):
        self._numero_saques += valor
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({"tipo": transacao.__name__, "valor": transacao.valor})

# =========================================================  Fim Conta  ========================================================#


# =====================================================  Inicio Transacao  ===================================================== #

class Transacao(ABC):
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        self.conta = conta
        pass

    @property
    @abstractmethod
    def valor(self, _valor):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if Deposito.valor > 0:
            conta.saldo = Deposito.valor
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, _valor):
        self._valor = _valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if self.valor > 0 and self.valor < conta.saldo:
            conta.saldo = -self.valor
            conta.numero_saques = 1
            conta.historico.adicionar_transacao(self)

# ======================================================  Fim Transacao  ======================================================= #

def mostrar_menu_inicial():
    opcao = input("""
---------------------------------------------------
Digite o numero do seu CPF ou conta para entrar.
[c] Cadastra Usuário        [l] Listar Usuário
                  
                  
[q] Sair
---------------------------------------------------
→ """)
    return opcao

def mostrar_menu_cliente(cliente):
    opcao = input(f"""
Bem vindo, {cliente.nome}!
---------------------------------------------------
Digite o numero conta para entrar.
[c] Cadastra nova conta     [l] Listar contas


[q] Voltar
---------------------------------------------------
→ """)
    
    return opcao

def mostrar_menu_conta(conta):
    opcao = input(f"""
Bem vindo(a), {conta.cliente.nome}!
---------------------------------------------------
Saldo Atual: R$ {conta.saldo:.2f}

[s] Sacar                   [d] Depositar
[e] Extrato

[q] Sair da conta
---------------------------------------------------
→ """)
    
    return opcao

def validar_cpf(cpf):
    pattern_cpf = "[0-9]{3}[.][0-9]{3}[.][0-9]{3}[-][0-9]{2}"

    if re.match(pattern_cpf, cpf):
        return True
    else:
        return False

def mensagem_valor_invalido():
    print("\n"+"".center(50, "="))
    print("Valor invalido!".center(51, " "))
    print("".center(51, "="))
    input("\nPressione <Enter> para continuar.")

def mensagem_Saldo_insuficiente():
    print("\n"+"".center(50, "="))
    print("Saldo insuficiente!".center(51, " "))
    print("".center(51, "="))  
    input("\nPressione <Enter> para continuar.")  

def cadastrar_usuario():
    cpf_encontrado = False

    while True:

        cpf = str(input("\nInforme seu CPF ou [q] para cancelar:\n→ "))
        if validar_cpf(cpf):

            # Procurando CPF
            cpf_encontrado = False
            for usuario in usuarios:
                if usuario.cpf == cpf:
                    cpf_encontrado = True
                    break

            if cpf_encontrado == True:
                print("\n"+" Cadastro falhou! ".center(51, "="))
                print("CPF já Cadastrado.".center(51, " "))
                print("".center(51, "="))
                input("\nPressione <Enter> para continuar.")
                break
            else:
                nome = str(input("Informe seu nome completo:\n→ "))
                data_nascimento = str(input("Informe a sua data de nascimento(dd/mm/aaaa):\n→ "))
                endereco = str(input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado):\n→ "))


                usuario = PessoaFisica.novo_cliente(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
                usuarios.append(usuario)
                print("\n"+"".center(50, "="))
                print("Usuário Cadastrado com sucesso!".center(51, " "))
                print("".center(51, "="))
                input("\nPressione <Enter> para continuar.")
                break
        # Sair
        elif cpf == "q": 
            break
        
        # Opção formato invalido.
        else:
            print("\n"+" CPF inválido! ".center(51,"="))
            print("  Use o formato XXX.XXX.XXX-XX  ".center(51,"="))
            print("".center(51,"="))

def cadastrar_conta(cliente):
    print("def cadastrar_conta")
    conta = ContaCorrente.nova_conta(numero=int(len(todas_contas)), cliente=cliente)

    cliente.contas.append(conta)
    todas_contas.append(conta)
    print("\n"+" Sucesso! ".center(51,"=")+"\n"+" Conta foi Cadastrada. ".center(51," "))
    print(f" Agencia: {conta.agencia}   Conta: {conta.numero} ".center(51," "))
    print("".center(51,"="))
    input("\nPressione <Enter> para continuar.")

def listar_usuarios(): # opção lu
    print(f"\n")
    for cliente in usuarios:
        print(f"[Cliente: {cliente.nome} - CPF:{cliente.cpf} - Data de nascimento: {cliente.data_nascimento} - Endereço: {cliente.endereco}]")
    input("\nPressione <Enter> para continuar.")

def listar_contas(cliente): # opção lc
    print(f"\n")
    x = 0
    for conta in cliente.contas:
        print(f"[Cliente: {conta.cliente.nome} - Agencia: {conta.agencia} - Conta: {conta.numero} - Saldo: R$ {cliente.contas[x].saldo:.2f} - Limite: R$ {cliente.contas[x].limite:.2f} - Saques realizados: {cliente.contas[x].numero_saques}]")
        x += 1
    input("\nPressione <Enter> para continuar.")

def menu_cliente(cliente):
    while True:
        opcao = mostrar_menu_cliente(cliente)
                            
        # Casdatra conta
        if opcao == "c":
            cadastrar_conta(cliente)
            opcao = None
                            
        # listar contas
        elif opcao == "l":
            listar_contas(cliente)
            opcao = None

        # Sair
        elif opcao == "q":
            opcao = None
            break

        # menu_conta
        else:
            for conta in todas_contas:
                if str(opcao) == str(conta.numero):
                    menu_conta(conta)
                    opcao = None
                    break

def menu_conta(conta):
    while True:
        opcao = mostrar_menu_conta(conta)

        # Depósito
        if opcao == "d":
            while True:

                try:
                    resposta = float(input("\nInforme o valor do depósito:\nR$ "))
                    if resposta > 0:
                        Deposito.valor = resposta
                        Deposito.registrar(Deposito, conta)
                        print("\n"+"".center(51, "="))
                        print(" Deposito realizado com sucesso! ".center(51, " "))
                        print("".center(51, "="))
                        input("\nPressione <Enter> para continuar.")
                        break
                    else:
                        mensagem_valor_invalido()
                        break
                    
                except ValueError:
                    mensagem_valor_invalido()
                    break
            
            opcao = None

        # Saque
        elif opcao == "s":
            while True:

                try:
                    resposta = float(input("\nInforme o valor do saque:\nR$ "))
                    if conta.numero_saques >= conta.limite_saques:
                        print("\n"+" Sague falhou! ".center(51, "="))
                        print("Limite de saques alcançado.".center(51, " "))
                        print("".center(51, "="))
                        input("\nPressione <Enter> para continuar.")
                        break

                    elif resposta > conta.limite:
                        print("\n"+" Sague falhou! ".center(51, "="))
                        print(f"Valor maior que o limite da conta.".center(51, " "))
                        print(f"Seu limite é R$ {conta.limite:.2f}".center(51, " "))
                        print("".center(51, "="))
                        input("\nPressione <Enter> para continuar.")
                        break

                    elif resposta >= conta.saldo:
                        mensagem_Saldo_insuficiente()
                        break

                    elif resposta > 0:
                        Saque.valor = resposta
                        Saque.registrar(Saque, conta)
                        print("\n"+"".center(51, "="))
                        print(" Sague realizado com sucesso! ".center(51, " "))
                        print("".center(51, "="))
                        input("\nPressione <Enter> para continuar.")
                        break

                    else:
                        mensagem_valor_invalido()
                        break
                    
                except ValueError:
                    mensagem_valor_invalido()
                    break
            
            opcao = None

        # Extrato
        elif opcao == "e":
            print(" Extrato ".center(51, "="))
            for transacao in conta.historico.transacoes:
                print(f"{transacao["tipo"]}: R$ {transacao["valor"]:.2f}")
            print(f"\nSaldo Atual: R$ {conta.saldo:.2f}\n"+"".center(51, "="))
            input("\nPressione <Enter> para continuar.")
            opcao = None

        # Sair
        elif opcao == "q":
            opcao = None
            break

def main():
    while True:

        opcao = mostrar_menu_inicial()

        # Casdatra usuário
        if opcao == "c":
            cadastrar_usuario()
            opcao = None

        # listar usuarios
        elif opcao == "l":
            listar_usuarios()
            opcao = None

        # Sair
        elif opcao == "q":
            break
        
        # Outros menus
        else:
            # menu_cliente
            if validar_cpf(opcao):
                for cliente in usuarios:
                    if str(opcao) == str(cliente.cpf):
                        menu_cliente(cliente)
                        opcao = None
                        break

            else:
                 # menu_conta
                for conta in todas_contas:
                    if str(opcao) == str(conta.numero):
                        menu_conta(conta)
                        opcao = None
                        break
                
                # Opção Invalida
                if opcao != None:
                    mensagem_valor_invalido()
                    opcao = None


main()
