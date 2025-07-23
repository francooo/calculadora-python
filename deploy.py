import os
import zipfile
import boto3
import json
import time

def criar_pacote_lambda():
    """Cria o pacote ZIP para o AWS Lambda"""
    print("Criando pacote Lambda...")
    
    # Arquivos a serem incluídos no pacote
    arquivos = [
        'lambda_function.py',
        'db_manager.py'
    ]
    
    # Cria o arquivo ZIP
    with zipfile.ZipFile('calculadora-lambda.zip', 'w') as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo)
    
    print("Pacote Lambda criado com sucesso: calculadora-lambda.zip")

def criar_tabela_dynamodb(nome_tabela='CalculadoraHistorico', regiao='us-east-1'):
    """Cria a tabela no DynamoDB se ela não existir"""
    print(f"Verificando/criando tabela DynamoDB: {nome_tabela}...")
    
    # Inicializa o cliente do DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=regiao)
    
    # Verifica se a tabela já existe
    tabelas_existentes = [tabela.name for tabela in dynamodb.tables.all()]
    
    if nome_tabela in tabelas_existentes:
        print(f"Tabela {nome_tabela} já existe.")
        return
    
    # Cria a tabela
    tabela = dynamodb.create_table(
        TableName=nome_tabela,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Chave de partição
            },
            {
                'AttributeName': 'timestamp',
                'KeyType': 'RANGE'  # Chave de classificação
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    # Espera até que a tabela exista
    print("Aguardando a criação da tabela...")
    tabela.meta.client.get_waiter('table_exists').wait(TableName=nome_tabela)
    print(f"Tabela {nome_tabela} criada com sucesso!")

def atualizar_lambda(nome_funcao='calculadora-api', regiao='us-east-1'):
    """Atualiza a função Lambda existente"""
    print(f"Atualizando função Lambda: {nome_funcao}...")
    
    # Inicializa o cliente do Lambda
    lambda_client = boto3.client('lambda', region_name=regiao)
    
    # Verifica se a função existe
    try:
        lambda_client.get_function(FunctionName=nome_funcao)
        
        # Atualiza o código da função
        with open('calculadora-lambda.zip', 'rb') as zipf:
            lambda_client.update_function_code(
                FunctionName=nome_funcao,
                ZipFile=zipf.read()
            )
        
        # Atualiza a configuração da função para incluir a variável de ambiente
        lambda_client.update_function_configuration(
            FunctionName=nome_funcao,
            Environment={
                'Variables': {
                    'DYNAMODB_TABLE': 'CalculadoraHistorico'
                }
            }
        )
        
        print(f"Função Lambda {nome_funcao} atualizada com sucesso!")
        
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"Função Lambda {nome_funcao} não encontrada. Crie a função primeiro.")
        print("Instruções para criar a função Lambda:")
        print("1. Acesse AWS Console > Lambda")
        print("2. Clique 'Create function'")
        print("3. Escolha 'Author from scratch'")
        print(f"4. Nome: {nome_funcao}")
        print("5. Runtime: Python 3.9+")
        print("6. Clique 'Create function'")
        print("7. Na função criada, vá em 'Code'")
        print("8. Clique 'Upload from' > '.zip file'")
        print("9. Selecione 'calculadora-lambda.zip'")
        print("10. Clique 'Save'")
        print("11. Em 'Configuration' > 'Environment variables', adicione DYNAMODB_TABLE=CalculadoraHistorico")

def configurar_permissoes_iam(nome_funcao='calculadora-api', regiao='us-east-1'):
    """Configura as permissões IAM para a função Lambda acessar o DynamoDB"""
    print(f"Configurando permissões IAM para a função Lambda: {nome_funcao}...")
    
    # Inicializa os clientes
    lambda_client = boto3.client('lambda', region_name=regiao)
    iam = boto3.client('iam', region_name=regiao)
    
    try:
        # Obtém o ARN do role da função Lambda
        response = lambda_client.get_function(FunctionName=nome_funcao)
        role_arn = response['Configuration']['Role']
        role_name = role_arn.split('/')[-1]
        
        # Cria a política para acesso ao DynamoDB
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:PutItem",
                        "dynamodb:GetItem",
                        "dynamodb:Scan",
                        "dynamodb:Query",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem"
                    ],
                    "Resource": f"arn:aws:dynamodb:{regiao}:*:table/CalculadoraHistorico"
                }
            ]
        }
        
        # Anexa a política ao role
        try:
            response = iam.put_role_policy(
                RoleName=role_name,
                PolicyName='CalculadoraDynamoDBAccess',
                PolicyDocument=json.dumps(policy_document)
            )
            print(f"Permissões IAM configuradas com sucesso para a função {nome_funcao}!")
        except Exception as e:
            print(f"Erro ao configurar permissões IAM: {e}")
            print("Você precisará configurar manualmente as permissões para a função Lambda acessar o DynamoDB.")
            print("Instruções:")
            print("1. Acesse AWS Console > IAM > Roles")
            print(f"2. Encontre o role associado à função Lambda {nome_funcao}")
            print("3. Clique em 'Add permissions' > 'Create inline policy'")
            print("4. Selecione o serviço 'DynamoDB'")
            print("5. Em 'Actions', selecione 'PutItem', 'GetItem', 'Scan', 'Query', 'UpdateItem', 'DeleteItem'")
            print("6. Em 'Resources', selecione 'Specific' e adicione a tabela 'CalculadoraHistorico'")
            print("7. Clique em 'Review policy'")
            print("8. Nome da política: 'CalculadoraDynamoDBAccess'")
            print("9. Clique em 'Create policy'")
    
    except Exception as e:
        print(f"Erro ao obter informações da função Lambda: {e}")
        print("Você precisará configurar manualmente as permissões para a função Lambda acessar o DynamoDB.")

def main():
    """Função principal para o deploy"""
    print("=== Iniciando deploy da Calculadora para AWS ===")
    
    # Cria o pacote Lambda
    criar_pacote_lambda()
    
    # Pergunta se deseja continuar com o deploy para AWS
    resposta = input("Deseja fazer o deploy para AWS? (s/n): ")
    if resposta.lower() != 's':
        print("Deploy para AWS cancelado.")
        return
    
    # Pergunta a região
    regiao = input("Digite a região AWS (padrão: us-east-1): ") or 'us-east-1'
    
    # Pergunta o nome da função Lambda
    nome_funcao = input("Digite o nome da função Lambda (padrão: calculadora-api): ") or 'calculadora-api'
    
    # Pergunta o nome da tabela DynamoDB
    nome_tabela = input("Digite o nome da tabela DynamoDB (padrão: CalculadoraHistorico): ") or 'CalculadoraHistorico'
    
    # Cria a tabela DynamoDB
    try:
        criar_tabela_dynamodb(nome_tabela, regiao)
    except Exception as e:
        print(f"Erro ao criar tabela DynamoDB: {e}")
        print("Você pode criar a tabela manualmente pelo console da AWS.")
    
    # Atualiza a função Lambda
    try:
        atualizar_lambda(nome_funcao, regiao)
    except Exception as e:
        print(f"Erro ao atualizar função Lambda: {e}")
    
    # Configura as permissões IAM
    try:
        configurar_permissoes_iam(nome_funcao, regiao)
    except Exception as e:
        print(f"Erro ao configurar permissões IAM: {e}")
    
    print("\n=== Deploy concluído! ===")
    print(f"Tabela DynamoDB: {nome_tabela}")
    print(f"Função Lambda: {nome_funcao}")
    print("\nPara testar a API, use os seguintes exemplos:")
    print("\nOperação básica:")
    print("""
{
  "operacao": "somar",
  "numero1": 10,
  "numero2": 5
}
    """)
    
    print("\nEquação de segundo grau:")
    print("""
{
  "operacao": "equacao_segundo_grau",
  "a": 1,
  "b": -5,
  "c": 6
}
    """)
    
    print("\nPara obter o histórico, configure um endpoint GET em /historico")

if __name__ == "__main__":
    main()