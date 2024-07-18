from abc import ABC, abstractmethod
from datetime import datetime
import re

# ==========================================================  Inicio Cliente  ========================================================= #
usuarios = []

class ContasIterador:
    def __init__(self):
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if len(todas_contas) > self.index:
            conta = todas_contas[self.index]
            self.index += 1
            return f"""\
Cliente: {conta.cliente.nome}
CPF:     {conta.cliente.cpf}
Agencia: {conta.agencia} Conta: {conta.numero}
Saldo: R$ {conta.saldo:.2f}
Limite: R$ {conta.limite:.2f}
Saques realizados: {conta.numero_saques}
---------------------------------------------------\
"""
        else:
            self.index = 0
            raise StopIteration

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

# ===========================================================  Fim Cliente  =========================================================== #

# =======================================================  Inicio Classe Conta  ======================================================= #
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

# ============================================================  Fim Conta  ============================================================ #

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append({"tipo": transacao.__name__, "valor": transacao.valor, "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})

    def gerar_relatorio(self, tipo_transacao):
        for transacao in self.transacoes:
            if  tipo_transacao == None:
                yield transacao

            elif tipo_transacao.__name__ == transacao["tipo"]:
                yield transacao

# =========================================================  Inicio Transação  ======================================================== #

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
        if self.valor > 0 and self.valor <= conta.saldo:
            conta.saldo = -self.valor
            conta.numero_saques = 1
            conta.historico.adicionar_transacao(self)

# ==========================================================  Fim Transação  ========================================================== #

def mostrar_menu_inicial():
    opcao = input("""
---------------------------------------------------
Digite o numero do seu CPF ou conta para entrar.
[c] Cadastra Usuário        [o] Opções de ADM


[q] Sair
---------------------------------------------------
→ """)
    return opcao

def mostrar_menu_adm():
    print(f"""
---------------------------------------------------
Nº de Usuários: {len(usuarios)}""", end="")
    for x in range(12-len(str(len(usuarios)))):
        print(" ", end="")
    opcao = input(f"""Nº de contas: {len(todas_contas)}
[u] Listar todos Usuários   [c] Listar todas contas


[q] Sair
---------------------------------------------------
→ """)
    return opcao

def mostrar_menu_cliente(cliente):
    opcao = input(f"""
Bem vindo(a), {cliente.nome.split(" ")[0]}!
---------------------------------------------------
Digite o numero conta para entrar.
[c] Cadastra nova conta     [l] Listar contas


[q] Voltar
---------------------------------------------------
→ """)
    
    return opcao

def mostrar_menu_conta(conta):
    opcao = input(f"""
Bem vindo(a), {conta.cliente.nome.split(" ")[0]}!
---------------------------------------------------
Saldo Atual: R$ {conta.saldo:.2f}

[s] Sacar                   [d] Depositar

[p] Extrato personalizado
[e] Extrato

[q] Sair da conta
---------------------------------------------------
→ """)
    
    return opcao

def mostrar_menu_extrato(conta):
    opcao = input(f"""
Bem vindo(a), {conta.cliente.nome.split(" ")[0]}!
---------------------------------------------------
Saldo Atual: R$ {conta.saldo:.2f}
[s] Somente Saques          [d] Somente Depositos
[t] Todas Transações


[q] voltar
---------------------------------------------------
→ """)
    
    return opcao

def log_transacao(funcao):
    def envelope(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        print(f"\n{re.sub("_"," ",funcao.__name__.upper())}", end="")
        for x in range(32-len(funcao.__name__)):
            print(" ", end="")
        print(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")
        print("".center(51, "="))  
        input("\nPressione <Enter> para continuar.")
        return resultado
    return envelope

def validar_cpf(cpf):
    pattern_cpf = "[0-9]{3}[.][0-9]{3}[.][0-9]{3}[-][0-9]{2}"

    if re.match(pattern_cpf, cpf):
        return True
    else:
        return False

# ============================ funções com decorador de Log =========================== #

@log_transacao
def extrato(conta, tipo_transacao):
    print(" Extrato ".center(51, "="))
    print(f"Cliente: {conta.cliente.nome}")
    print(f"Agência: {conta.agencia} Conta:{conta.numero}")
    print("".center(51, "-"))
    for transacao in conta.historico.gerar_relatorio(tipo_transacao):
        print(f"{transacao["tipo"]}:", end="")
        for espaco in range(12-len(f"{transacao["tipo"]}")):
            print(" ", end="")
        print(f"R$ {transacao["valor"]:.2f}", end="")
        for espaco in range(19-len(str(f"R$ {transacao["valor"]:.2f}"))):
            print(" ", end="")
        print(f"{transacao["data"]}")

    print(f"\nSaldo Atual: R$ {conta.saldo:.2f}\n")

@log_transacao
def deposito(conta):
    while True:

        try:
            resposta = float(input("\nInforme o valor do depósito:\nR$ "))
            if resposta > 0:
                Deposito.valor = resposta
                Deposito.registrar(Deposito, conta)
                print("\n"+"".center(51, "="))
                print(" Deposito realizado com sucesso! ".center(51, " "))
                print(f" Valor: R$ {Deposito.valor:.2f} ".center(51, " "))
                break

            else:
                print("\n"+"".center(50, "="))
                print("Valor invalido!".center(51, " "))
                break
                    
        except ValueError:
            print("\n"+" Erro! ".center(50, "="))
            print("Valor invalido!".center(51, " "))
            break

@log_transacao
def saque(conta):
    while True:

        try:
            resposta = float(input("\nInforme o valor do saque:\nR$ "))
            if conta.numero_saques >= conta.limite_saques:
                print("\n"+" Sague falhou! ".center(51, "="))
                print("Limite de saques alcançado.".center(51, " "))
                break

            elif resposta > conta.limite:
                print("\n"+" Sague falhou! ".center(51, "="))
                print(f"Valor maior que o limite da conta.".center(51, " "))
                print(f"Seu limite é de R$ {conta.limite:.2f}".center(51, " "))
                break

            elif resposta > conta.saldo:
                print("\n"+"".center(50, "="))
                print("Saldo insuficiente!".center(51, " "))
                break

            elif resposta > 0:
                Saque.valor = resposta
                Saque.registrar(Saque, conta)
                print("\n"+"".center(51, "="))
                print(" Sague realizado com sucesso! ".center(51, " "))
                print(f" Valor: R$ {Saque.valor:.2f} ".center(51, " "))
                break

            else:
                print("\n"+"".center(50, "="))
                print("Valor invalido!".center(51, " "))
                break
                    
        except ValueError:
            print("\n"+" Erro! ".center(50, "="))
            print("Valor invalido!".center(51, " "))
            break

@log_transacao
def cadastrar_usuario():
    cpf_encontrado = False

    # Pedir CPF.
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
                print("\n"+" Erro! ".center(51, "="))
                print(" CPF já Cadastrado. ".center(51," "))
                break

            else:

                # Pedir nome completo.
                while True:
                    resposta = str.strip(input("Informe seu nome completo:\n→ "))

                    if len(re.sub("[a-zA-ZáàâãéèêíïóôõöúüçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÜÇÑ ]","",resposta)) > 0:
                        print("\n"+" Atênção! ".center(51, "="))
                        print("Favor, não inclua caracteres especiais ou numeros.".center(51, " "))
                        print("".center(51, "="))
                        input("\nPressione <Enter> para continuar.")

                    elif len(resposta.split(" ")) > 1:
                        nome = (resposta.title())
                        break
                        
                    else:
                        print("\n"+" Atênção! ".center(51, "="))
                        print("Favor, informe o nome completo.".center(51, " "))
                        print("".center(51, "="))
                        input("\nPressione <Enter> para continuar.")

                # Pedir data de nascimento.
                while True:
                    validar_data = True
                    data_nascimento = str(input("Informe a sua data de nascimento(dd/mm/aaaa):\n→ "))
                    if re.match("[0-3][0-9][/][0-1][0-9][/][0-9][0-9][0-9][0-9]", data_nascimento):
                        for x in (data_nascimento.split("/")):
                            if int(x) == 0:
                                validar_data = False
                                break
                        if validar_data:
                            break

                        else:
                            print("\n"+" Erro! ".center(51, "="))
                            print("Favor, informe uma data válida.".center(51, " "))
                            print("".center(51, "="))
                            input("\nPressione <Enter> para continuar.")

                    else:
                        print("\n"+" Atênção! ".center(51, "="))
                        print("Favor, utilizar o formato dd/mm/aaaa.".center(51, " "))
                        print("".center(51, "="))
                        input("\nPressione <Enter> para continuar.")

                # Pedir data de nascimento.
                endereco = str(input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado):\n→ "))

                # Sucesso!
                usuario = PessoaFisica.novo_cliente(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
                usuarios.append(usuario)
                print("\n"+"".center(51, "="))
                print("Usuário Cadastrado com sucesso!".center(51, " "))
                break
        # Cancelar.
        elif cpf == "q": 
            print("\n"+"".center(51, "="))
            print("Cadastrado cancelado".center(51, " "))
            break
        
        # Opção CPF em formato inválido.
        else:
            print("\n"+" CPF inválido! ".center(51,"="))
            print("  Use o formato XXX.XXX.XXX-XX  ".center(51," "))
            print("".center(51,"="))
            input("\nPressione <Enter> para continuar.")

@log_transacao
def cadastrar_conta(cliente):
    print("def cadastrar_conta")
    conta = ContaCorrente.nova_conta(numero=int(len(todas_contas)), cliente=cliente)

    cliente.contas.append(conta)
    todas_contas.append(conta)
    print("\n"+" Sucesso! ".center(51,"=")+"\n"+" Conta foi Cadastrada. ".center(51," "))
    print(f" Agencia: {conta.agencia}   Conta: {conta.numero} ".center(51," "))

@log_transacao
def listar_usuarios():
    if len(usuarios) == 0:
        print("\n"+"".center(51, "="))
        print("Nenhum usuário encontrado!".center(51, " "))

    else:
        print(" Clientes ".center(51,"=")+"\n"+"".center(51,"-"))
        for cliente in usuarios:
            print(f"Cliente: {cliente.nome}")
            print(f"CPF:{cliente.cpf}")
            print(f"Data de nascimento: {cliente.data_nascimento}")
            print(f"Endereço: {cliente.endereco}")
            print("".center(51,"-"))
        print("\n",len(usuarios)," usuário encontrado."if(len(usuarios)== 1)else" usuários encontrados.", sep="")

@log_transacao
def listar_todas_contas(todas_contas):
    if len(todas_contas) == 0:
        print("\n"+"".center(51, "="))
        print("Nenhuma conta encontrada!".center(51, " "))

    else:
        print(" Contas ".center(51,"=")+"\n"+"".center(51,"-"))
        for conta in ContasIterador():
            print(conta)
        print("\n",len(todas_contas)," conta encontrada."if(len(todas_contas)== 1)else" contas encontradas.", sep="")

@log_transacao
def listar_contas(cliente):
    if len(cliente.contas) == 0:
        print("\n"+"".center(51, "="))
        print("Nenhuma conta encontrada!".center(51, " "))

    else:
        print(" Contas ".center(51,"=")+"\n"+"".center(51,"-"))
        for x, conta in enumerate(cliente.contas):
            print(f"Cliente: {conta.cliente.nome}")
            print(f"Agencia: {conta.agencia} Conta: {conta.numero}")
            print(f"Saldo: R$ {cliente.contas[x].saldo:.2f}")
            print(f"Limite: R$ {cliente.contas[x].limite:.2f}")
            print(f"Saques realizados: {cliente.contas[x].numero_saques}")
            print("".center(51,"-"))
        print("\n",len(cliente.contas)," conta encontrada."if(len(cliente.contas)== 1)else" contas encontradas.", sep="")

# ==================================== Fim de Logs ==================================== #

def menu_extrato(conta):
    while True:
        opcao = mostrar_menu_extrato(conta)

        # Exibi Saques
        if opcao == "s":
            extrato(conta, Saque)
            opcao = None 

        # Exibi Depositos
        elif opcao == "d":
            extrato(conta, Deposito)
            opcao = None 

        # Exibi todas transações
        elif opcao == "t":
            extrato(conta, None)
            opcao = None 

        # Sair.
        elif opcao == "q":
            opcao = None
            break

def menu_cliente(cliente):
    while True:
        opcao = mostrar_menu_cliente(cliente)
                            
        # Casdatra conta.
        if opcao == "c":
            cadastrar_conta(cliente)
            opcao = None
                            
        # listar contas.
        elif opcao == "l":
            listar_contas(cliente)
            opcao = None

        # Sair.
        elif opcao == "q":
            opcao = None
            break

        # menu_conta.
        else:
            for conta in todas_contas:
                if str(opcao) == str(conta.numero):
                    menu_conta(conta)
                    opcao = None
                    break

def menu_conta(conta):
    while True:
        opcao = mostrar_menu_conta(conta)

        # Depósito.
        if opcao == "d":
            deposito(conta)
            opcao = None

        # Saque.
        elif opcao == "s":
            saque(conta)
            opcao = None

        # Extrato personalizado.
        elif opcao == "p":
            menu_extrato(conta)
            opcao = None

        # Extrato.
        elif opcao == "e":
            extrato(conta, None)
            opcao = None

        # Sair.
        elif opcao == "q":
            opcao = None
            break

def menu_adm():
    while True:
        opcao = mostrar_menu_adm()

        # Listar todas contas.
        if opcao == "c":
            listar_todas_contas(todas_contas)
            opcao = None

        # Listar usuários.
        if opcao == "u":
            listar_usuarios()
            opcao = None
        
        # Sair.
        elif opcao == "q":
            break

def main():
    while True:

        opcao = mostrar_menu_inicial()

        # Casdatra usuário.
        if opcao == "c":
            cadastrar_usuario()
            opcao = None

        # Menu adm.
        elif opcao == "o":
            menu_adm()
            opcao = None

        # Sair.
        elif opcao == "q":
            break
        
        # Outros menus.
        else:
            # menu_cliente.
            if validar_cpf(opcao):
                for cliente in usuarios:
                    if str(opcao) == str(cliente.cpf):
                        menu_cliente(cliente)
                        opcao = None
                        break

                if opcao != None:
                    print("\n"+" CPF não cadastrado! ".center(51, "="))
                    print("Cadastre um usuário um novo.".center(51, " "))
                    print("".center(51, "="))
                    input("\nPressione <Enter> para continuar.")

            else:
                # menu_conta.
                for conta in todas_contas:
                    if str(opcao) == str(conta.numero):
                        menu_conta(conta)
                        opcao = None
                        break
                
                # Opção Invalida.
                if opcao != None:
                    print("\n"+"".center(50, "="))
                    print("Valor invalido!".center(51, " "))
                    opcao = None

main()
