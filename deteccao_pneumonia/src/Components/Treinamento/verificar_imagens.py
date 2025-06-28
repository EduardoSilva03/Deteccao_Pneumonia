from PIL import Image
import os

def verificar_imagens(diretorio):
    erros = []
    for root, _, files in os.walk(diretorio):
        for file in files:
            caminho = os.path.join(root, file)
            try:
                with Image.open(caminho) as img:
                    img.verify()
            except Exception as e:
                print(f"[ERRO] Arquivo inválido removido: {caminho} - {e}")
                erros.append(caminho)
                os.remove(caminho)
    print(f"\nTotal de imagens inválidas removidas: {len(erros)}")

verificar_imagens("../../Images")