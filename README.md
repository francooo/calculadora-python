# Calculadora - Múltiplas Versões

Calculadora completa com versões Python, Web e AWS. Inclui resolução de equações de segundo grau com processamento de imagens.

## 📁 Estrutura do Projeto

```
calculadora-python/
├── calculadora.py          # Versão Python console
├── processador_imagem.py   # Processamento de imagens para equações
├── requirements.txt        # Dependências Python
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
# Instalar dependências
pip install -r requirements.txt

# Executar a calculadora
python calculadora.py
```

> **Nota**: Para usar a funcionalidade de processamento de imagens, é necessário instalar o Tesseract OCR: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

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
- ✅ Resolução de equações de segundo grau
- ✅ Processamento de imagens para extrair equações
- ✅ Exibição detalhada das etapas de resolução
- ✅ Tratamento de erros
- ✅ Interface console (Python)
- ✅ Interface web responsiva
- ✅ API REST
- ✅ Deploy AWS Lambda
- ✅ Validação completa

## 🛠️ Tecnologias

- **Python**: Console + Lambda
- **Tesseract OCR**: Processamento de imagens
- **Node.js**: Web server + Lambda
- **HTML/CSS/JS**: Frontend
- **AWS**: Lambda + API Gateway
- **Express**: Web framework