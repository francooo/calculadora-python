exports.handler = async (event) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    };
    
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers };
    }
    
    try {
        const { numero1, numero2, operacao } = JSON.parse(event.body);
        
        const a = parseFloat(numero1);
        const b = parseFloat(numero2);
        
        if (isNaN(a) || isNaN(b)) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ erro: 'Números inválidos' })
            };
        }
        
        let resultado;
        switch(operacao) {
            case 'somar': resultado = a + b; break;
            case 'subtrair': resultado = a - b; break;
            case 'multiplicar': resultado = a * b; break;
            case 'dividir':
                if (b === 0) {
                    return {
                        statusCode: 400,
                        headers,
                        body: JSON.stringify({ erro: 'Divisão por zero' })
                    };
                }
                resultado = a / b;
                break;
            default:
                return {
                    statusCode: 400,
                    headers,
                    body: JSON.stringify({ erro: 'Operação inválida' })
                };
        }
        
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ operacao, numero1: a, numero2: b, resultado })
        };
        
    } catch (error) {
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ erro: 'Erro interno' })
        };
    }
};