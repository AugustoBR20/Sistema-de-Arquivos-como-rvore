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

def arquivos_maiores_que(no, limite):
    resultados = []

    def buscar(n):
        if n.eh_arquivo and n.tamanho > limite:
            resultados.append(n)
        elif not n.eh_arquivo:
            for f in n.filhos:
                buscar(f)
    buscar(no)
    return resultados

def pasta_com_mais_arquivos(no): # Define os parâmetros
    melhor_pasta = None # Cria variável local para armazenar a pasta com mais arquivos, começa vazia
    max_qtd = -1 # Cria variável para armazenar a maior quantidade de arquivos encontrada em uma pasta (começa com -1)
                 # para garantir que mesmo que a pasta encontrada tenha 0 arquivos, ela ainda será considerada.
    def buscar(n): # Função recursiva para buscar a pasta com mais arquivos
        nonlocal melhor_pasta, max_qtd # Usa nonlocal para modificar as variáveis melhor_pasta e max_qtd, dentro de uma função interna
        if not n.eh_arquivo: # Checa se n não é um arquivo, 
            qtd = sum(1 for f in n.filhos if f.eh_arquivo or f.filhos) # Conta quantos filhos o nó tem que são arquivos ou possuem  filhos (arquivos ou subpastas)
            if qtd > max_qtd: # Se essa quantidade qtd for maior que max_qtd
                melhor_pasta = n # Atualiza melhor_pasta
                max_qtd = qtd # Atualiza max_qtd
            for f in n.filhos: # Para cada filho chama buscar recursivamente
                buscar(f)
    buscar(no) # Percorre recursivamente toda a árvore de diretórios e arquivos, começando pelo nó passado como argumento
    return melhor_pasta, max_qtd # Retorna a pasta com mais arquivos e a quantidade encontrada

def arquivos_por_extensao(no, extensao): # Define os parâmetros
    encontrados = [] # Lista para armazenar os arquivos encontrados

    def buscar(n): #Função recursiva para buscar arquivos com a extensão especificada
        if n.eh_arquivo and n.nome.endswith(extensao): # Verifica se é um arquivo e se termina com a extensão informada
            encontrados.append(n) # Caso o if seja True, ele insere o nó à lista "encontrados"
        else: # Caso o contrário, percorre todos os filhos e chama a função de busca recursivamente para cada filho
            for f in n.filhos:
                buscar(f)

    buscar(no) # Inicia a busca a partir do nó raiz passado como argumento.
    return encontrados # Retorna a lista com os arquivos encontrados que possuem a extensão desejada

