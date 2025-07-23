import json
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys

# Adiciona o diretório atual ao path para importar módulos locais
sys.path.append(os.getcwd())

# Importa o gerenciador de banco de dados
try:
    from db_manager import CalculadoraDB
    # Inicializa o banco de dados
    db = CalculadoraDB()
    db.criar_tabela_se_nao_existir()
    DB_DISPONIVEL = True
except Exception as e:
    print(f"Aviso: Não foi possível inicializar o banco de dados: {e}")
    DB_DISPONIVEL = False

# Importar a função de resolver equação de segundo grau da calculadora
from calculadora import resolver_equacao_segundo_grau

class ServidorCalculadora(BaseHTTPRequestHandler):
    def do_GET(self):
        # Rota para obter o histórico
        if self.path.startswith('/historico'):
            self.enviar_historico()
            return
            
        # Rota para obter um cálculo específico
        if self.path.startswith('/calculo/'):
            calc_id = self.path.split('/calculo/')[1]
            self.enviar_calculo(calc_id)
            return
            
        # Servir arquivos estáticos
        if self.path == '/':
            self.path = '/teste_local.html'
            
        try:
            file_path = os.path.join(os.getcwd(), self.path[1:])
            with open(file_path, 'rb') as file:
                content = file.read()
                self.send_response(200)
                
                if self.path.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif self.path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif self.path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                    
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f"Arquivo não encontrado: {self.path}")
            
    def enviar_historico(self):
        """Envia o histórico de cálculos como JSON"""
        if not DB_DISPONIVEL:
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"erro": "Banco de dados não disponível"}).encode('utf-8'))
            return
            
        try:
            # Extrai o parâmetro limite da URL se existir
            limite = 10
            if '?' in self.path and 'limite=' in self.path:
                limite_str = self.path.split('limite=')[1].split('&')[0]
                try:
                    limite = int(limite_str)
                except ValueError:
                    pass
                    
            historico = db.obter_historico(limite=limite)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"historico": historico}, default=str).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"erro": str(e)}).encode('utf-8'))
    
    def enviar_calculo(self, calc_id):
        """Envia um cálculo específico como JSON"""
        if not DB_DISPONIVEL:
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"erro": "Banco de dados não disponível"}).encode('utf-8'))
            return
            
        try:
            calculo = db.obter_calculo_por_id(calc_id)
            
            if calculo:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(calculo, default=str).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"erro": f"Cálculo com ID {calc_id} não encontrado"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"erro": str(e)}).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/calcular':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            response = self.processar_calculo(data)
            
            # Registra o cálculo no banco de dados se disponível
            if DB_DISPONIVEL:
                try:
                    operacao = data.get('operacao')
                    
                    if operacao in ['somar', 'subtrair', 'multiplicar', 'dividir']:
                        entrada = {
                            'numero1': data.get('numero1'),
                            'numero2': data.get('numero2')
                        }
                    elif operacao == 'equacao_segundo_grau':
                        entrada = {
                            'a': data.get('a'),
                            'b': data.get('b'),
                            'c': data.get('c')
                        }
                    
                    calc_id = db.registrar_calculo(operacao, entrada, response.get('resultado'))
                    response['id'] = calc_id
                except Exception as e:
                    print(f"Erro ao registrar no banco de dados: {e}")
                    response['db_error'] = str(e)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, default=str).encode('utf-8'))
    
    def processar_calculo(self, data):
        operacao = data.get('operacao')
        
        try:
            # Operações básicas
            if operacao in ['somar', 'subtrair', 'multiplicar', 'dividir']:
                a = float(data.get('numero1'))
                b = float(data.get('numero2'))
                
                if operacao == 'somar':
                    resultado = a + b
                elif operacao == 'subtrair':
                    resultado = a - b
                elif operacao == 'multiplicar':
                    resultado = a * b
                elif operacao == 'dividir':
                    if b == 0:
                        return {'erro': 'Divisão por zero não permitida'}
                    resultado = a / b
                    
                return {
                    'operacao': operacao,
                    'numero1': a,
                    'numero2': b,
                    'resultado': resultado
                }
            
            # Equação de segundo grau
            elif operacao == 'equacao_segundo_grau':
                a = float(data.get('a'))
                b = float(data.get('b'))
                c = float(data.get('c'))
                
                if a == 0:
                    return {'erro': 'O coeficiente "a" não pode ser zero (não seria uma equação de segundo grau)'}
                
                # Calcular o discriminante (delta)
                delta = b**2 - 4*a*c
                
                # Etapas da resolução
                etapas = [
                    f"Equação: {a}x² + {b}x + {c} = 0",
                    f"1. Calculando o discriminante: Δ = b² - 4ac = {b}² - 4 × {a} × {c} = {delta}"
                ]
                
                # Verificar o valor de delta
                if delta < 0:
                    etapas.append(f"2. Como Δ = {delta} < 0, a equação não possui raízes reais.")
                    return {
                        'operacao': operacao,
                        'coeficientes': {'a': a, 'b': b, 'c': c},
                        'resultado': {
                            'delta': delta,
                            'raizes': [],
                            'etapas': etapas,
                            'mensagem': "A equação não possui raízes reais."
                        }
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
                    raizes = [x1]
                else:
                    etapas.append(f"3. A equação possui duas raízes reais: x₁ = {x1:.4f} e x₂ = {x2:.4f}")
                    mensagem = "A equação possui duas raízes reais."
                    raizes = [x1, x2]
                
                return {
                    'operacao': operacao,
                    'coeficientes': {'a': a, 'b': b, 'c': c},
                    'resultado': {
                        'delta': delta,
                        'raizes': raizes,
                        'etapas': etapas,
                        'mensagem': mensagem
                    }
                }
            
            else:
                return {'erro': 'Operação inválida'}
                
        except Exception as e:
            return {'erro': str(e)}

def iniciar_servidor(porta=8000):
    servidor = HTTPServer(('localhost', porta), ServidorCalculadora)
    print(f"Servidor iniciado em http://localhost:{porta}")
    print("Pressione Ctrl+C para encerrar")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()