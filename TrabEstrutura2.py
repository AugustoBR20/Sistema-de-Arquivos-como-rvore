import os
import sys

def mostrar_arvore(caminho, nivel=0):
    if os.path.isdir(caminho):
        filhos = os.listdir(caminho)
        total = 0
        for f in filhos:
            caminho_completo = os.path.join(caminho, f)
            total += calcular_tamanho(caminho_completo)
        print("  " * nivel + f"{os.path.basename(caminho)} ({len(filhos)} filhos, {total} bytes)")
        for f in filhos:
            mostrar_arvore(os.path.join(caminho, f), nivel + 1)
    elif os.path.isfile(caminho):
        print("  " * nivel + f"{os.path.basename(caminho)} ({os.path.getsize(caminho)} bytes)")

