import os
import sys

class No:
    def __init__(self, caminho):
        self.caminho = caminho
        self.nome = os.path.basename(caminho)
        self.eh_arquivo = os.path.isfile(caminho)
        self.filhos = []
        self.tamanho = 0

        if os.path.islink(caminho) or not (os.path.isdir(caminho) or os.path.isfile(caminho)):
            return

        if self.eh_arquivo:
            self.tamanho = os.path.getsize(caminho)
        else:
            self.carregar_filhos()
            self.tamanho = sum(f.tamanho for f in self.filhos)

    def carregar_filhos(self):
        try:
            for item in os.listdir(self.caminho):
                caminho_completo = os.path.join(self.caminho, item)
                no_filho = No(caminho_completo)
                if no_filho.eh_arquivo or no_filho.filhos is not None:
                    self.filhos.append(no_filho)
        except PermissionError:
            pass

def exibir_arvore(no, nivel=0):
    prefixo = "│   " * nivel + ("├── " if nivel > 0 else "")
    if no.eh_arquivo:
        print(f"{prefixo}{no.nome} ({no.tamanho} bytes)")
    else:
        print(f"{prefixo}{no.nome} ({len(no.filhos)} filhos, {no.tamanho} bytes)")
        for filho in no.filhos:
            exibir_arvore(filho, nivel + 1)

def exportar_html(no, nivel=0):
    html = ""
    indent = "&nbsp;" * (nivel * 4)
    if no.eh_arquivo:
        html += f"{indent}{no.nome} ({no.tamanho} bytes)<br>\n"
    else:
        html += f"{indent}<b>{no.nome}</b> ({len(no.filhos)} filhos, {no.tamanho} bytes)<br>\n"
        for filho in no.filhos:
            html += exportar_html(filho, nivel + 1)
    return html

def salvar_html(conteudo):
    with open("saida.html", "w") as f:
        f.write("<html><body>\n" + conteudo + "</body></html>")
    print("Exportado para 'saida.html'.")

def encontrar_maior_arquivo(no, maiores=None, max_tam=0):
    if maiores is None:
        maiores = []

    if no.eh_arquivo:
        if no.tamanho > max_tam:
            return [no], no.tamanho
        elif no.tamanho == max_tam:
            maiores.append(no)
    else:
        for filho in no.filhos:
            maiores, max_tam = encontrar_maior_arquivo(filho, maiores, max_tam)
    return maiores, max_tam
