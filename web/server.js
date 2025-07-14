const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static('.'));

app.post('/api/calcular', (req, res) => {
    try {
        const { numero1, numero2, operacao } = req.body;
        
        const a = parseFloat(numero1);
        const b = parseFloat(numero2);
        
        if (isNaN(a) || isNaN(b)) {
            return res.status(400).json({ erro: 'Números inválidos' });
        }
        
        let resultado;
        switch(operacao) {
            case 'somar':
                resultado = a + b;
                break;
            case 'subtrair':
                resultado = a - b;
                break;
            case 'multiplicar':
                resultado = a * b;
                break;
            case 'dividir':
                if (b === 0) {
                    return res.status(400).json({ erro: 'Divisão por zero não permitida' });
                }
                resultado = a / b;
                break;
            default:
                return res.status(400).json({ erro: 'Operação inválida' });
        }
        
        res.json({
            operacao,
            numero1: a,
            numero2: b,
            resultado
        });
        
    } catch (error) {
        res.status(500).json({ erro: 'Erro interno do servidor' });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});