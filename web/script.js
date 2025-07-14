async function calcular() {
    const num1 = parseFloat(document.getElementById('num1').value);
    const num2 = parseFloat(document.getElementById('num2').value);
    const operacao = document.getElementById('operacao').value;
    const resultado = document.getElementById('resultado');
    
    if (isNaN(num1) || isNaN(num2)) {
        resultado.innerHTML = '<span style="color: red;">Digite números válidos!</span>';
        return;
    }
    
    try {
        const response = await fetch('/api/calcular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                numero1: num1,
                numero2: num2,
                operacao: operacao
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultado.innerHTML = `<span style="color: green; font-size: 1.2em;">${data.resultado}</span>`;
        } else {
            resultado.innerHTML = `<span style="color: red;">${data.erro}</span>`;
        }
    } catch (error) {
        // Fallback para cálculo local se API não estiver disponível
        let res;
        switch(operacao) {
            case 'somar': res = num1 + num2; break;
            case 'subtrair': res = num1 - num2; break;
            case 'multiplicar': res = num1 * num2; break;
            case 'dividir': 
                if (num2 === 0) {
                    resultado.innerHTML = '<span style="color: red;">Divisão por zero!</span>';
                    return;
                }
                res = num1 / num2; 
                break;
        }
        resultado.innerHTML = `<span style="color: green; font-size: 1.2em;">${res}</span>`;
    }
}