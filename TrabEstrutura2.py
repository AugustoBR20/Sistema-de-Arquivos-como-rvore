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

def calcular_tamanho(caminho):
    if os.path.isfile(caminho):
        return os.path.getsize(caminho)
    elif os.path.isdir(caminho):
        total = 0
        for item in os.listdir(caminho):
            total += calcular_tamanho(os.path.join(caminho, item))
        return total
    return 0

def exportar_html(caminho, nivel=0):
    html = ""
    if os.path.isdir(caminho):
        filhos = os.listdir(caminho)
        total = 0
        for f in filhos:
            total += calcular_tamanho(os.path.join(caminho, f))
        html += "&nbsp;" * (nivel * 4) + f"<b>{os.path.basename(caminho)}</b> ({len(filhos)} filhos, {total} bytes)<br>\n"
        for f in filhos:
            html += exportar_html(os.path.join(caminho, f), nivel + 1)
    elif os.path.isfile(caminho):
        html += "&nbsp;" * (nivel * 4) + f"{os.path.basename(caminho)} ({os.path.getsize(caminho)} bytes)<br>\n"
    return html
