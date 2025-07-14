# Deploy da Calculadora na AWS Lambda

## Arquivos criados:
- `lambda_function.py` - Função Lambda da calculadora
- `calculadora-lambda.zip` - Pacote para upload

## Como fazer o deploy:

### 1. Criar função Lambda:
- Acesse AWS Console > Lambda
- Clique "Create function"
- Escolha "Author from scratch"
- Nome: `calculadora-api`
- Runtime: Python 3.9+
- Clique "Create function"

### 2. Upload do código:
- Na função criada, vá em "Code"
- Clique "Upload from" > ".zip file"
- Selecione `calculadora-lambda.zip`
- Clique "Save"

### 3. Testar a função:
```json
{
  "operacao": "somar",
  "numero1": 10,
  "numero2": 5
}
```

### 4. Criar API Gateway (opcional):
- Services > API Gateway
- Create API > REST API
- Conectar à função Lambda

## Operações disponíveis:
- `somar`, `subtrair`, `multiplicar`, `dividir`

## Exemplo de resposta:
```json
{
  "operacao": "somar",
  "numero1": 10,
  "numero2": 5,
  "resultado": 15
}
```