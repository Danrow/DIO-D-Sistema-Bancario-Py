LIMITE_SAQUES = 3
AGENCIA = "0001"
usuarios = []
contas = []

def funcao_deposito(saldo, extrato,/):
    
    valor = float(input("\nInforme o valor do depósito:\nR$ "))

    #Depósito efetuado.
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: +R$ {valor:.2f}\n"
            
    #Valor invalido.
    else:
        print("\nOperação falhou!\nValor invalido.")
    
    return saldo, extrato

def funcao_sague(* ,saldo, limite, extrato, numero_saques, LIMITE_SAQUES):
    valor = float(input("\nInforme o valor do saque:\nR$ "))

    #Saque excedeu o saldo.
    if valor > saldo: 
        print("\nOperação falhou!\nValor do sague excede o saldo da conta.")

    #Saque excedeu limite de R$500,00.
    elif valor > limite: 
        print("\nOperação falhou!\nValor do sague excede o limite de R$500,00.")

    #Excedeu limite diario do sagues.
    elif numero_saques >= LIMITE_SAQUES: 
        print("\nOperação falhou!\nNúmero máximo de saques diários foi excedido.")

    #Sague efetuado.
    elif valor > 0: 
        saldo -= valor
        extrato += f"Saque:    -R$ {valor:.2f}\n"
        numero_saques += 1

    #Valor invalido.
    else: 
        print("\nOperação falhou!\nValor invalido. \n")
        
    return saldo, extrato, numero_saques

def funcao_extrato(saldo, /, *, extrato):
    print("\n"+" Extrato ".center(33,"="))
    print(f"\n{extrato}" if extrato != "" else "\nNão houve movimentação na conta.")
    print(f"Saldo em conta: R$ {saldo:.2f}\n")
    print("".center(33,"="))

def funcao_casdatra_usuario():
    cpf = str(input("\nInforme seu CPF:\n→ "))
    for usuario in usuarios:
        if usuario["CPF"] == cpf:
            print("\n"+" Cadastro falhou! ".center(51,"=")+"\n"+" CPF já Cadastrado. ".center(51,"="))
            return

    nome = str(input("Informe seu nome completo:\n→ "))
    data_nascimento = str(input("Informe a sua data de nascimento(dd/mm/aaaa):\n→ "))
    endereco = str(input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado):\n→ "))

    usuarios.append({"CPF": cpf, "nome":nome, "data_nascimento":data_nascimento, "endereco":endereco})
    print("\n"+" Usuário Cadastrado com sucesso! ".center(51,"="))

def funcao_casdatra_conta():
    while True:
        cpf = str(input("\nInforme seu CPF ou digite [q] para cancelar\n→ "))
        if cpf == "q":
            break
        else:
            cpf_localizado = False
            cpf_localizado = [True for usuario in usuarios if cpf in usuario["CPF"]]
            
            if cpf_localizado:
                contas.append({"CPF": cpf, "Agencia": AGENCIA, "conta": str(len(contas)+1), "saldo": 0, "limite": 500, "numero_saques": 0, "extrato": ""})
                print("\n"+" Sucesso! ".center(51,"=")+"\n"+" Conta foi Cadastrada. ".center(51,"="))
                print(f"\n Agencia: {AGENCIA}   Conta: " + contas[(len(contas)-1)]["conta"])
                
            else:
                print("\n" + " CPF não encontrado. ".center(51,"="))
                print(" Por favor cadastre um usuário. ".center(51,"="))
        return

def funcao_menu_inicial():
    opcao = input("""
---------------------------------------------------
Digite o numero da conta para entrar.
[u] Cadastra Usuário    [c] Cadastra Conta
[l] Listar Contas

[q] Sair
---------------------------------------------------
→ """)
    return opcao

def funcao_menu_conta():
    for usuario in usuarios:
        if usuario["CPF"] == conta["CPF"]:
            opcao = input(f"""
Bem vindo, {usuario["nome"]}!
---------------------------------------------------
[s] Sacar                   [d] Depositar
[e] Extrato
                  
[q] Sair da conta
---------------------------------------------------
→ """)
    
    return opcao

while True:
    opcao = funcao_menu_inicial()
    
    # Opção - Casdatra usuario
    if opcao == "u":
        funcao_casdatra_usuario()
    
    # Opção - Casdatra conta
    elif opcao == "c":
        funcao_casdatra_conta()

    # Opção - Listar contas
    elif opcao == "l":
        for conta in contas:
            print(conta)

    # Opção - Sair
    elif opcao == "q":
        break

    else:
        
        # Opção Inválida - Não à usuários Cadatrados
        if len(contas) == 0:
            print("\n"+" Operação inválida! ".center(51,"=")+"\n"+" Não à contas cadatradas. ".center(51,"="))

        # Opção - Entrar na conta com CPF
        else:
            opcao_invalida = True # Essa variavel impede que a menssagem de opção inválida se mostre de forma incorreta depois do "for".
            for conta in contas:

                # menu da conta
                if opcao in conta["conta"]:
                    while True:
                        opcao = funcao_menu_conta()

                        # Depósito
                        if opcao == "d":
                            conta["saldo"], conta["extrato"] = funcao_deposito(conta["saldo"], conta["extrato"])

                        # Saque
                        elif opcao == "s":
                            conta["saldo"], conta["extrato"], conta["numero_saques"] = funcao_sague(saldo=conta["saldo"], limite=conta["limite"], extrato=conta["extrato"], numero_saques=conta["numero_saques"], LIMITE_SAQUES=LIMITE_SAQUES)

                        # Extrato
                        elif opcao == "e":
                            funcao_extrato(conta["saldo"], extrato=conta["extrato"])

                        #Sair
                        elif opcao == "q":
                            opcao_invalida = False
                            break
            
            # Opção Inválida
            if opcao_invalida:
                print("\n"+" Operação inválida! ".center(51,"="))
                print(" Por favor selecione novamente a operação desejada.".center(51,"="))
                print("".center(51,"="))
