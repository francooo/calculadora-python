import boto3
import uuid
from datetime import datetime
import json

class CalculadoraDB:
    def __init__(self, table_name='CalculadoraHistorico', region='us-east-1'):
        """
        Inicializa o gerenciador de banco de dados para a calculadora.
        
        Args:
            table_name (str): Nome da tabela no DynamoDB
            region (str): Região da AWS
        """
        self.table_name = table_name
        self.region = region
        
        # Inicializa o cliente do DynamoDB
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.table = self.dynamodb.Table(self.table_name)
    
    def criar_tabela_se_nao_existir(self):
        """Cria a tabela no DynamoDB se ela não existir."""
        try:
            # Verifica se a tabela já existe
            self.dynamodb.meta.client.describe_table(TableName=self.table_name)
            print(f"Tabela {self.table_name} já existe.")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            # Cria a tabela se não existir
            print(f"Criando tabela {self.table_name}...")
            
            table = self.dynamodb.create_table(
                TableName=self.table_name,
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
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f"Tabela {self.table_name} criada com sucesso!")
    
    def registrar_calculo(self, operacao, entrada, resultado):
        """
        Registra um cálculo no histórico.
        
        Args:
            operacao (str): Tipo de operação realizada
            entrada (dict): Dados de entrada do cálculo
            resultado (any): Resultado do cálculo
            
        Returns:
            str: ID do registro criado
        """
        # Gera um ID único para o registro
        calc_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Prepara o item para inserção
        item = {
            'id': calc_id,
            'timestamp': timestamp,
            'operacao': operacao,
            'entrada': json.dumps(entrada),
            'resultado': json.dumps(resultado, default=str)
        }
        
        # Insere o item na tabela
        self.table.put_item(Item=item)
        
        print(f"Cálculo registrado com ID: {calc_id}")
        return calc_id
    
    def obter_historico(self, limite=10):
        """
        Obtém os registros mais recentes do histórico.
        
        Args:
            limite (int): Número máximo de registros a retornar
            
        Returns:
            list: Lista de registros do histórico
        """
        response = self.table.scan(Limit=limite)
        items = response.get('Items', [])
        
        # Converte os dados JSON de volta para objetos Python
        for item in items:
            if 'entrada' in item:
                item['entrada'] = json.loads(item['entrada'])
            if 'resultado' in item:
                item['resultado'] = json.loads(item['resultado'])
        
        # Ordena por timestamp (mais recente primeiro)
        items.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return items
    
    def obter_calculo_por_id(self, calc_id):
        """
        Obtém um cálculo específico pelo ID.
        
        Args:
            calc_id (str): ID do cálculo
            
        Returns:
            dict: Registro do cálculo ou None se não encontrado
        """
        # Como precisamos do timestamp para a chave composta, fazemos um scan com filtro
        response = self.table.scan(
            FilterExpression=boto3.dynamodb.conditions.Key('id').eq(calc_id)
        )
        
        items = response.get('Items', [])
        if not items:
            return None
        
        item = items[0]
        
        # Converte os dados JSON de volta para objetos Python
        if 'entrada' in item:
            item['entrada'] = json.loads(item['entrada'])
        if 'resultado' in item:
            item['resultado'] = json.loads(item['resultado'])
        
        return item