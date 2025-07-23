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

### 4. Criar API Gateway (opcional):
- Services > API Gateway
- Create API > REST API
- Conectar à função Lambda

## Operações disponíveis:
- `somar`, `subtrair`, `multiplicar`, `dividir`
- `equacao_segundo_grau`

## Exemplos de resposta:

**Operação básica:**
```json
{
  "operacao": "somar",
  "numero1": 10,
  "numero2": 5,
  "resultado": 15
}
```

**Equação de segundo grau:**
```json
{
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