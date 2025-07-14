def calculadora():
    while True:
        print("\n=== CALCULADORA ===")
        print("1. Somar")
        print("2. Subtrair") 
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Sair")
        
        opcao = input("Escolha uma opção (1-5): ")
        
        if opcao == '5':
            print("Saindo...")
            break
            
        if opcao not in ['1', '2', '3', '4']:
            print("Opção inválida!")
            continue
            
        try:
            a = float(input("Digite o primeiro número: "))
            b = float(input("Digite o segundo número: "))
            
            if opcao == '1':
                print(f"Resultado: {a + b}")
            elif opcao == '2':
                print(f"Resultado: {a - b}")
            elif opcao == '3':
                print(f"Resultado: {a * b}")
            elif opcao == '4':
                if b == 0:
                    print("Erro: Divisão por zero!")
                else:
                    print(f"Resultado: {a / b}")
        except ValueError:
            print("Erro: Digite apenas números!")

if __name__ == "__main__":
    calculadora()