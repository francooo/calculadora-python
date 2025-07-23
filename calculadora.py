import math
import os
from processador_imagem import extrair_equacao_da_imagem

def resolver_equacao_segundo_grau(a, b, c):
    """Resolve uma equação de segundo grau ax² + bx + c = 0 usando a fórmula de Bhaskara"""
    print(f"\nResolvendo a equação: {a}x² + {b}x + {c} = 0")
    print("\nEtapas da resolução:")
    
    # Etapa 1: Calcular o discriminante (delta)
    delta = b**2 - 4*a*c
    print(f"1. Calculando o discriminante (delta):\n   Δ = b² - 4ac\n   Δ = {b}² - 4 × {a} × {c}\n   Δ = {b**2} - {4*a*c}\n   Δ = {delta}")
    
    # Etapa 2: Verificar o valor de delta
    if delta < 0:
        print(f"2. Como Δ = {delta} < 0, a equação não possui raízes reais.")
        return None, None
    
    # Etapa 3: Calcular as raízes
    x1 = (-b + math.sqrt(delta)) / (2*a)
    x2 = (-b - math.sqrt(delta)) / (2*a)
    
    print(f"2. Como Δ = {delta} ≥ 0, calculamos as raízes:")
    print(f"   x₁ = (-b + √Δ) / 2a\n   x₁ = (-{b} + √{delta}) / (2 × {a})\n   x₁ = ({-b} + {math.sqrt(delta):.4f}) / {2*a}\n   x₁ = {x1:.4f}")
    print(f"   x₂ = (-b - √Δ) / 2a\n   x₂ = (-{b} - √{delta}) / (2 × {a})\n   x₂ = ({-b} - {math.sqrt(delta):.4f}) / {2*a}\n   x₂ = {x2:.4f}")
    
    # Etapa 4: Conclusão
    if delta == 0:
        print(f"3. Como Δ = 0, a equação possui uma única raiz real: x = {x1:.4f}")
    else:
        print(f"3. A equação possui duas raízes reais: x₁ = {x1:.4f} e x₂ = {x2:.4f}")
    
    return x1, x2

def calculadora():
    while True:
        print("\n=== CALCULADORA ===")
        print("1. Somar")
        print("2. Subtrair") 
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Resolver equação de segundo grau (ax² + bx + c = 0)")
        print("6. Resolver equação de segundo grau a partir de uma imagem")
        print("7. Sair")
        
        opcao = input("Escolha uma opção (1-7): ")
        
        if opcao == '7':
            print("Saindo...")
            break
            
        if opcao not in ['1', '2', '3', '4', '5', '6']:
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
            elif opcao == '5':
                try:
                    print("\nDigite os coeficientes da equação ax² + bx + c = 0:")
                    a = float(input("a = "))
                    if a == 0:
                        print("Erro: O coeficiente 'a' não pode ser zero (não seria uma equação de segundo grau)")
                        continue
                    b = float(input("b = "))
                    c = float(input("c = "))
                    resolver_equacao_segundo_grau(a, b, c)
                except ValueError:
                    print("Erro: Digite apenas números!")
            elif opcao == '6':
                try:
                    print("\nProcessando equação de segundo grau a partir de uma imagem")
                    caminho_imagem = input("Digite o caminho completo da imagem: ")
                    
                    if not os.path.exists(caminho_imagem):
                        print(f"Erro: O arquivo '{caminho_imagem}' não existe!")
                        continue
                        
                    print("Processando a imagem...")
                    coeficientes = extrair_equacao_da_imagem(caminho_imagem)
                    
                    if coeficientes:
                        a, b, c = coeficientes
                        print(f"Equação identificada: {a}x² + {b}x + {c} = 0")
                        resolver_equacao_segundo_grau(a, b, c)
                    else:
                        print("Não foi possível extrair uma equação válida da imagem.")
                except Exception as e:
                    print(f"Erro ao processar a imagem: {e}")
                    print("Dica: Certifique-se de que a biblioteca pytesseract está instalada e configurada corretamente.")
                    print("Instale com: pip install pytesseract pillow")
                    print("E instale o Tesseract OCR: https://github.com/tesseract-ocr/tesseract")
        except ValueError:
            print("Erro: Digite apenas números!")

if __name__ == "__main__":
    calculadora()