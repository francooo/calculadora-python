import json

def lambda_handler(event, context):
    try:
        body = json.loads(event['body']) if event.get('body') else event
        
        operacao = body.get('operacao')
        a = float(body.get('numero1'))
        b = float(body.get('numero2'))
        
        if operacao == 'somar':
            resultado = a + b
        elif operacao == 'subtrair':
            resultado = a - b
        elif operacao == 'multiplicar':
            resultado = a * b
        elif operacao == 'dividir':
            if b == 0:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'erro': 'Divisão por zero não permitida'})
                }
            resultado = a / b
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'erro': 'Operação inválida'})
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'operacao': operacao,
                'numero1': a,
                'numero2': b,
                'resultado': resultado
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'erro': str(e)})
        }