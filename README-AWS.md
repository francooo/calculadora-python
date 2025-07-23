# Deploy da Calculadora na AWS Lambda

## Arquivos criados:
- `lambda_function.py` - Função Lambda da calculadora
- `db_manager.py` - Gerenciador de banco de dados DynamoDB
- `calculadora-lambda.zip` - Pacote para upload
- `deploy.py` - Script de automatização de deploy

## Como fazer o deploy:

### Opção 1: Deploy automatizado

```bash
# Instalar dependências
pip install boto3

# Executar script de deploy
python deploy.py
```

O script `deploy.py` vai:
1. Criar o pacote ZIP para o Lambda
2. Criar a tabela DynamoDB (se não existir)
3. Atualizar a função Lambda (se existir)
4. Configurar as permissões IAM necessárias

### Opção 2: Deploy manual

#### 1. Criar tabela DynamoDB:
- Acesse AWS Console > DynamoDB
- Clique "Create table"
- Nome: `CalculadoraHistorico`
- Chave de partição: `id` (String)
- Chave de classificação: `timestamp` (String)
- Clique "Create table"

#### 2. Criar função Lambda:
- Acesse AWS Console > Lambda
- Clique "Create function"
- Escolha "Author from scratch"
- Nome: `calculadora-api`
- Runtime: Python 3.9+
- Clique "Create function"

#### 3. Upload do código:
- Na função criada, vá em "Code"
- Clique "Upload from" > ".zip file"
- Selecione `calculadora-lambda.zip`
- Clique "Save"

#### 4. Configurar variáveis de ambiente:
- Na função Lambda, vá em "Configuration" > "Environment variables"
- Adicione: `DYNAMODB_TABLE` = `CalculadoraHistorico`

#### 5. Configurar permissões IAM:
- Na função Lambda, vá em "Configuration" > "Permissions"
- Clique no role da função
- Adicione uma política inline para acesso ao DynamoDB

### 3. Testar a função:

**Operação básica:**
```json
{
  "operacao": "somar",
  "numero1": 10,
  "numero2": 5
}
```

**Equação de segundo grau:**
```json
{
  "operacao": "equacao_segundo_grau",
  "a": 1,
  "b": -5,
  "c": 6
}
```

### 4. Criar API Gateway:
- Services > API Gateway
- Create API > REST API
- Crie os seguintes endpoints:
  - POST `/calcular` - Conectado à função Lambda
  - GET `/historico` - Conectado à função Lambda
  - GET `/calculo/{id}` - Conectado à função Lambda

## Operações disponíveis:
- `somar`, `subtrair`, `multiplicar`, `dividir`
- `equacao_segundo_grau`

## Exemplos de resposta:

**Operação básica:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "operacao": "somar",
  "numero1": 10,
  "numero2": 5,
  "resultado": 15
}
```

**Equação de segundo grau:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "operacao": "equacao_segundo_grau",
  "coeficientes": {"a": 1, "b": -5, "c": 6},
  "resultado": {
    "delta": 1,
    "raizes": [3.0, 2.0],
    "etapas": [
      "Equação: 1x² + -5x + 6 = 0",
      "1. Calculando o discriminante: Δ = b² - 4ac = -5² - 4 × 1 × 6 = 1",
      "2. Como Δ = 1 ≥ 0, calculamos as raízes:",
      "   x₁ = (-b + √Δ) / 2a = (-(-5) + √1) / (2 × 1) = 3.0000",
      "   x₂ = (-b - √Δ) / 2a = (-(-5) - √1) / (2 × 1) = 2.0000",
      "3. A equação possui duas raízes reais: x₁ = 3.0000 e x₂ = 2.0000"
    ],
    "mensagem": "A equação possui duas raízes reais."
  }
}
```

**Histórico de cálculos:**
```json
{
  "historico": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "timestamp": "2023-07-23T18:45:12.123456",
      "operacao": "equacao_segundo_grau",
      "entrada": {"a": 1, "b": -5, "c": 6},
      "resultado": {
        "delta": 1,
        "raizes": [3.0, 2.0],
        "mensagem": "A equação possui duas raízes reais."
      }
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2023-07-23T18:40:05.654321",
      "operacao": "somar",
      "entrada": {"numero1": 10, "numero2": 5},
      "resultado": 15
    }
  ]
}
```