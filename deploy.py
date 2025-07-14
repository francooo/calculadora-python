import zipfile
import os

def criar_pacote_lambda():
    with zipfile.ZipFile('calculadora-lambda.zip', 'w') as zipf:
        zipf.write('lambda_function.py')
    print("Pacote calculadora-lambda.zip criado com sucesso!")
    print("\nPróximos passos:")
    print("1. Acesse o AWS Console")
    print("2. Vá para Lambda > Create function")
    print("3. Escolha 'Author from scratch'")
    print("4. Nome: calculadora-api")
    print("5. Runtime: Python 3.9+")
    print("6. Upload o arquivo calculadora-lambda.zip")

if __name__ == "__main__":
    criar_pacote_lambda()