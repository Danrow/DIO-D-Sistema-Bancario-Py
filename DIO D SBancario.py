from abc import ABC, abstractclassmethod, abstractproperty
import re

todas_contas = []
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
    
    def realizar_transacao(self, conta, transacao):
        pass

    def adicionar_conta(conta):
        pass

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

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        if self._saldo >= valor:
            print('O saque foi realizado com sucesso.')
            return True

        else:
            print('Não foi possível sacar!')
            return False

    def depositar(self, valor):
        if valor > 0:
            print('Deposito realizado com sucusso.')
        else:
            print('Não foi possível depositar!')

class ContaCorrente(Conta):
    def __init__(self,numero, cliente, limite = 500., limite_saques = 3):
        super().__init__(numero, cliente)
        self._numero_saques = 0
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        if (self._saldo >= valor) and (valor <= self._limite) and (self._numero_saques < self._limite_saques):
            print('O saque foi realizado com sucesso.')
            return True

        else:
            print('Não foi possível sacar!')
            return False

    def depositar(self, valor):
        if valor > 0:
            print('Deposito realizado com sucusso.')
        else:
            print('Não foi possível depositar!')
    
class Historico:
    def __init__(self):
        self.adicionar_transacao = ""

    def adicionar_transacao(self, transacao):
        # Depósito = True

        if transacao["tipo"] == "Depósito":
            self.adicionar_transacao += f"Depósito: +R$ {transacao["valor"]} - Agência: {transacao["Agência"]} Conta: {transacao["Conta"]}\n"
        
        # Saque = False
        if transacao["tipo"] == "Saque":
            transacao["tipo"]
            self.adicionar_transacao += f"Saque:    -R$ {transacao["valor"]} - Agência: {transacao["Agência"]} Conta: {transacao["Conta"]}\n"
        

class Transacao(ABC):
    @abstractclassmethod
    def registrar(self, conta):
        self.conta = conta
        pass

    @property
    @abstractproperty
    def valor(self, _valor):
        pass

class Deposito(Transacao):
    def __init__(self, _valor):
        self._valor = _valor

    @property
    def valor(self, _valor):
        self._valor = _valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.saldo += self.valor
            transacao = {"tipo": "Depósito", "valor": self.valor, "Agência": conta.agencia ,"Conta": conta.numero}
            Historico.adicionar_transacao(transacao)

class Saque(Transacao):
    def __init__(self, _valor):
        self._valor = _valor

    @property
    def valor(self, _valor):
        self._valor = _valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.saldo -= self.valor
            conta.numero_saques += 1
            transacao = {"tipo": "Saque", "valor": self.valor, "Agência": conta.agencia ,"Conta": conta.numero}
            Historico.adicionar_transacao(transacao)

def main():
    while True:

        opcao = menu_inicial()

        # Casdatra usuário
        if opcao == "u":
            casdatra_usuario()
            opcao = None

        # Casdatra conta
        if opcao == "c":
            casdatra_conta()
            opcao = None

        # listar usuarios
        if opcao == "lu":
            listar_usuarios()
            opcao = None

        # listar contas
        if opcao == "lc":
            listar_contas()
            opcao = None

        # Sair
        if opcao == "q":
            break
        
        for conta in todas_contas:
            if str(opcao) == str(conta.numero):

                while True:
                    opcao = menu_conta(conta)

                    # Depósito
                    if opcao == "d":
                        Deposito.valor = float(input("\nInforme o valor do depósito:\nR$ "))

                        Deposito.registrar(conta)
                        opcao = None

                    # Saque
                    elif opcao == "s":
                        Saque.valor = float(input("\nInforme o valor do depósito:\nR$ "))

                        Saque.registrar(conta)
                        opcao = None

                    # Extrato
                    elif opcao == "e":
                        opcao = None

                    # Sair
                    if opcao == "q":
                        opcao = None
                        break

def menu_inicial():
    opcao = input("""
---------------------------------------------------
Digite o numero da conta para entrar.
[u]  Cadastra Usuário    [c]  Cadastra Conta
                  
[lu] Listar Usuário      [lc] Listar Contas
[H]  Histórico
                  
[q] Sair
---------------------------------------------------
→ """)
    return opcao

def menu_conta(conta):
    opcao = input(f"""
Bem vindo, {conta.cliente.nome}!
---------------------------------------------------
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

def listar_usuarios():
    for usuario in usuarios:
        print(f'Nome: {usuario.nome} , CPF: {usuario.cpf}, Nascimento: {usuario.data_nascimento}, Endereço: {usuario.endereco}')

def listar_contas():
    for conta in todas_contas:
        print(f"Agencia: {conta.agencia} Conta: {conta.numero} Proprietario: {conta.cliente.nome}")

def casdatra_usuario():
    cpf_encontrado = False

    while True:

        cpf = str(input("\nInforme seu CPF ou [q] para cancelar:\n→ "))
        if validar_cpf(cpf):

            for usuario in usuarios:
                if usuario.cpf == cpf:
                    cpf_encontrado = True
                    break
                else:
                    cpf_encontrado = False

            if cpf_encontrado == True:
                print("\n"+" Cadastro falhou! ".center(51,"=")+"\n"+" CPF já Cadastrado. ".center(51,"="))

            else:
                nome = str(input("Informe seu nome completo:\n→ "))
                data_nascimento = str(input("Informe a sua data de nascimento(dd/mm/aaaa):\n→ "))
                endereco = str(input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado):\n→ "))

                usuario = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
                usuarios.append(usuario)
                print("\n"+" Usuário Cadastrado com sucesso! ".center(51,"="))
                break
        # Sair
        elif cpf == "q": 
            break
        
        # Opção formato invalido.
        else:
            print("\n"+" CPF inválido! ".center(51,"="))
            print("  Use o formato XXX.XXX.XXX-XX  ".center(51,"="))
            print("".center(51,"="))

def casdatra_conta():
    while True:
        cpf = str(input("\nInforme seu CPF ou digite [q] para cancelar:\n→ "))
        if cpf == "q":
            break
        
        # Opção formato invalido.
        elif validar_cpf(cpf) == False:
            print("\n"+" CPF inválido! ".center(51,"="))
            print("  Use o formato XXX.XXX.XXX-XX  ".center(51,"="))
            print("".center(51,"="))
            
        else:
            for usuario in usuarios:
                if usuario.cpf == cpf:
                    cpf_encontrado = True
                    break
                else:
                    cpf_encontrado = False

            # Cadastrando conta
            if cpf_encontrado == True:

                conta = Conta(numero=int(len(todas_contas)), cliente=usuario)


                usuario.contas.append(conta)
                todas_contas.append(conta)
                print("\n"+" Sucesso! ".center(51,"=")+"\n"+" Conta foi Cadastrada. ".center(51,"="))
                print(f" Agencia: {conta.agencia}   Conta: {conta.numero} ".center(51,"="))
                print("".center(51,"="))
                break
            
            # CPF não encontrado
            else:
                print("\n" + " CPF não encontrado. ".center(51,"="))
                print(" Por favor cadastre um usuário. ".center(51,"="))
        
            

main()