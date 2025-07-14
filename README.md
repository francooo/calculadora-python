# Calculadora - Múltiplas Versões

Calculadora completa com versões Python, Web e AWS.

## 📁 Estrutura do Projeto

```
calculadora-python/
├── calculadora.py          # Versão Python console
├── lambda_function.py      # Versão AWS Lambda (Python)
├── calculadora-lambda.zip  # Pacote Lambda Python
├── web/                    # Versão Web Full-Stack
│   ├── index.html         # Frontend
│   ├── style.css          # Estilos
│   ├── script.js          # JavaScript
│   ├── server.js          # Backend Node.js
│   ├── lambda-api.js      # Lambda Node.js
│   └── package.json       # Dependências
└── README-AWS.md          # Guia AWS
```

## 🚀 Versões Disponíveis

### 1. Python Console
```bash
python calculadora.py
```

### 2. Web Application
```bash
cd web
npm install
npm start
# Acesse: http://localhost:3000
```

### 3. AWS Lambda
- Upload `calculadora-lambda.zip` (Python)
- Upload `web/calculadora-web-lambda.zip` (Node.js)

## ✨ Funcionalidades

- ✅ Soma, Subtração, Multiplicação, Divisão
- ✅ Tratamento de erros
- ✅ Interface console (Python)
- ✅ Interface web responsiva
- ✅ API REST
- ✅ Deploy AWS Lambda
- ✅ Validação completa

## 🛠️ Tecnologias

- **Python**: Console + Lambda
- **Node.js**: Web server + Lambda
- **HTML/CSS/JS**: Frontend
- **AWS**: Lambda + API Gateway
- **Express**: Web framework