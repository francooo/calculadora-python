import json
import math
import os
from db_manager import CalculadoraDB

# Inicializa o gerenciador de banco de dados
db = CalculadoraDB(table_name=os.environ.get('DYNAMODB_TABLE', 'CalculadoraHistorico'))

# Tenta criar a tabela se estiver em ambiente de desenvolvimento
try:
    if os.environ.get('AWS_EXECUTION_ENV') is None:  # Não estamos no Lambda
        db.criar_tabela_se_nao_existir()
except Exception as e:
    print(f"Aviso: Não foi possível verificar/criar a tabela: {e}")

def resolver_equacao_segundo_grau(a, b, c):
    """Resolve uma equação de segundo grau ax² + bx + c = 0 usando a fórmula de Bhaskara"""
    # Calcular o discriminante (delta)
    delta = b**2 - 4*a*c
    
    # Etapas da resolução para retornar
    etapas = [
        f"Equação: {a}x² + {b}x + {c} = 0",
        f"1. Calculando o discriminante: Δ = b² - 4ac = {b}² - 4 × {a} × {c} = {delta}"
    ]
    
    # Verificar o valor de delta
    if delta < 0:
        etapas.append(f"2. Como Δ = {delta} < 0, a equação não possui raízes reais.")
        return {
            "delta": delta,
            "raizes": [],
            "etapas": etapas,
            "mensagem": "A equação não possui raízes reais."
        }
    
    # Calcular as raízes
    x1 = (-b + math.sqrt(delta)) / (2*a)
    x2 = (-b - math.sqrt(delta)) / (2*a)
    
    etapas.append(f"2. Como Δ = {delta} ≥ 0, calculamos as raízes:")
    etapas.append(f"   x₁ = (-b + √Δ) / 2a = (-{b} + √{delta}) / (2 × {a}) = {x1:.4f}")
    etapas.append(f"   x₂ = (-b - √Δ) / 2a = (-{b} - √{delta}) / (2 × {a}) = {x2:.4f}")
    
    # Conclusão
    if delta == 0:
        etapas.append(f"3. Como Δ = 0, a equação possui uma única raiz real: x = {x1:.4f}")
        mensagem = "A equação possui uma única raiz real."
    else:
        etapas.append(f"3. A equação possui duas raízes reais: x₁ = {x1:.4f} e x₂ = {x2:.4f}")
        mensagem = "A equação possui duas raízes reais."
    
    return {
        "delta": delta,
        "raizes": [x1, x2] if delta > 0 else [x1],
        "etapas": etapas,
        "mensagem": mensagem
    }

def lambda_handler(event, context):
    # Verifica se é uma solicitação para obter o histórico
    if event.get('httpMethod') == 'GET' and event.get('path', '').endswith('/historico'):
        try:
            limite = int(event.get('queryStringParameters', {}).get('limite', 10))
            historico = db.obter_historico(limite=limite)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'historico': historico
                }, default=str)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'erro': f'Erro ao obter histórico: {str(e)}'
                })
            }
    
    # Verifica se é uma solicitação para obter um cálculo específico
    if event.get('httpMethod') == 'GET' and '/calculo/' in event.get('path', ''):
        try:
            calc_id = event.get('path', '').split('/calculo/')[1]
            calculo = db.obter_calculo_por_id(calc_id)
            
            if calculo:
                return {
                    'statusCode': 200,
                    'body': json.dumps(calculo, default=str)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        'erro': f'Cálculo com ID {calc_id} não encontrado'
                    })
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'erro': f'Erro ao obter cálculo: {str(e)}'
                })
            }
    try:
        body = json.loads(event['body']) if event.get('body') else event
        
        operacao = body.get('operacao')
        
        # Operações básicas
        if operacao in ['somar', 'subtrair', 'multiplicar', 'dividir']:
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
                
            # Registra o cálculo no DynamoDB
            try:
                entrada = {'numero1': a, 'numero2': b}
                calc_id = db.registrar_calculo(operacao, entrada, resultado)
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'id': calc_id,
                        'operacao': operacao,
                        'numero1': a,
                        'numero2': b,
                        'resultado': resultado
                    })
                }
            except Exception as e:
                print(f"Erro ao registrar no DynamoDB: {e}")
                # Continua mesmo se falhar o registro
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'operacao': operacao,
                        'numero1': a,
                        'numero2': b,
                        'resultado': resultado,
                        'db_error': str(e)
                    })
                }
        
        # Resolução de equação de segundo grau
        elif operacao == 'equacao_segundo_grau':
            a = float(body.get('a'))
            b = float(body.get('b'))
            c = float(body.get('c'))
            
            if a == 0:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'erro': 'O coeficiente "a" não pode ser zero (não seria uma equação de segundo grau)'})
                }
            
            resultado = resolver_equacao_segundo_grau(a, b, c)
            
            # Registra o cálculo no DynamoDB
            try:
                entrada = {'a': a, 'b': b, 'c': c}
                calc_id = db.registrar_calculo(operacao, entrada, resultado)
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'id': calc_id,
                        'operacao': operacao,
                        'coeficientes': {'a': a, 'b': b, 'c': c},
                        'resultado': resultado
                    }, default=str)
                }
            except Exception as e:
                print(f"Erro ao registrar no DynamoDB: {e}")
                # Continua mesmo se falhar o registro
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'operacao': operacao,
                        'coeficientes': {'a': a, 'b': b, 'c': c},
                        'resultado': resultado,
                        'db_error': str(e)
                    }, default=str)
                }
        
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'erro': 'Operação inválida'})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'erro': str(e)})
        }