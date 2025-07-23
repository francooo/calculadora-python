import re
import pytesseract
from PIL import Image

# Configuração do Tesseract OCR (ajuste o caminho conforme necessário)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Descomente e ajuste se necessário

def extrair_equacao_da_imagem(caminho_imagem):
    """
    Extrai uma equação de segundo grau de uma imagem usando OCR.
    
    Args:
        caminho_imagem (str): Caminho para o arquivo de imagem
        
    Returns:
        tuple: Coeficientes (a, b, c) da equação ax² + bx + c = 0
    """
    try:
        # Abrir a imagem
        imagem = Image.open(caminho_imagem)
        
        # Extrair texto da imagem
        texto = pytesseract.image_to_string(imagem)
        print(f"Texto extraído da imagem: {texto}")
        
        # Procurar por padrões de equação de segundo grau
        # Padrão básico: ax² + bx + c = 0
        padrao = r'(-?\d*\.?\d*)x\^?2\s*([+-]\s*\d*\.?\d*)x\s*([+-]\s*\d*\.?\d*)\s*=\s*0'
        match = re.search(padrao, texto.replace(' ', ''))
        
        if match:
            # Extrair coeficientes
            a = float(match.group(1)) if match.group(1) and match.group(1) != '-' else (-1 if match.group(1) == '-' else 1)
            
            # Processar b (pode ter sinal + ou -)
            b_str = match.group(2).replace(' ', '')
            if b_str == '+': b = 1
            elif b_str == '-': b = -1
            else: b = float(b_str)
            
            # Processar c (pode ter sinal + ou -)
            c_str = match.group(3).replace(' ', '')
            if c_str == '+': c = 1
            elif c_str == '-': c = -1
            else: c = float(c_str)
            
            return a, b, c
        else:
            print("Não foi possível identificar uma equação de segundo grau na imagem.")
            return None
            
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None