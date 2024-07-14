menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

→ """
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    #Depósito
    if opcao == "d":
        valor = float(input("\nInforme o valor do depósito:\nR$ "))

        #Depósito efetuado.
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: +R$ {valor:.2f}\n"

        #Valor invalido.
        else:
            print("\nOperação falhou!\nValor invalido.")

    #Saque
    elif opcao == "s":

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

    #Extrato
    elif opcao == "e":
        print(" Extrato ".center(30,"=") + "\n")
        print(f"{extrato}\n" if extrato != "" else "Não houve movimentação na conta.")
        print(f"Saldo em conta: R$ {saldo:.2f}\n")
        print("".center(30,"="))

    #Sair
    elif opcao == "q":
        break

    #Inválido
    else:
        print("\nOperação inválida.\nPor favor selecione novamente a operação desejada.")