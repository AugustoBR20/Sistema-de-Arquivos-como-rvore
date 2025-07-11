import os  # Importa a biblioteca 'os', ela permite interações com o sistema de arquivos
import sys  # Importa a biblioteca 'sys', ela permite acessar argumentos passados pela linha de comando

class No:  # Define a classe 'No' que representa um arquivo ou diretório na árvore
    def __init__(self, caminho):  # Construtor da classe, recebe o caminho do arquivo ou diretório
        self.caminho = caminho  # Armazena o caminho completo do nó
        self.nome = os.path.basename(caminho)  # Extrai apenas o nome do arquivo ou pasta
        self.eh_arquivo = os.path.isfile(caminho)  # Verifica se o caminho é um arquivo
        self.eh_diretorio = os.path.isdir(caminho) # Verifica se o caminho é um diretório
        self.filhos = []  # Inicializa a lista de filhos (vazia)
        self.tamanho = 0  # Inicializa o tamanho como 0

        # Ignora links simbólicos e entradas que não sejam arquivos nem diretórios
        if os.path.islink(caminho) or not (os.path.isdir(caminho) or os.path.isfile(caminho)):
            return

        # Se for arquivo, pega seu tamanho
        if self.eh_arquivo:
            self.tamanho = os.path.getsize(caminho)
        else:
            self.carregar_filhos()  # Carrega os filhos de forma recursiva
            self.tamanho = sum(f.tamanho for f in self.filhos)  # Soma os tamanhos dos filhos

    def carregar_filhos(self):  # Função para carregar os filhos do diretório
        try:
            for item in os.listdir(self.caminho):  # Lista todos os itens do diretório
                caminho_completo = os.path.join(self.caminho, item)  # Cria o caminho completo do item
                no_filho = No(caminho_completo)  # Cria um novo nó filho
                if no_filho.eh_arquivo or no_filho.eh_diretorio:  # Verifica se o nó filho é válido
                    self.filhos.append(no_filho)  # Adiciona o nó filho à lista de filhos
        except PermissionError:  # Se não tiver permissão para acessar o diretório
            pass  # Ignora o erro e continua

def exibir_arvore(no, nivel=0):  # Função para exibir a árvore de diretórios no terminal
    prefixo = "│   " * nivel + ("├── " if nivel > 0 else "")  # Define o prefixo de indentação
    if no.eh_arquivo:  # Se for arquivo, exibe com tamanho
        print(f"{prefixo}{no.nome} ({no.tamanho} bytes)")
    else:  # Se for diretório, exibe com quantidade de filhos e tamanho total
        print(f"{prefixo}{no.nome} ({len(no.filhos)} filhos, {no.tamanho} bytes)")
        for filho in no.filhos:  # Para cada filho, chama recursivamente
            exibir_arvore(filho, nivel + 1)

def exportar_html(no, nivel=0):  # Função para gerar a árvore em HTML
    html = ""  # Inicializa a string HTML
    indent = "&nbsp;" * (nivel * 4)  # Define a indentação em HTML
    if no.eh_arquivo:  # Se for arquivo, adiciona linha simples
        html += f"{indent}{no.nome} ({no.tamanho} bytes)<br>\n"
    else:  # Se for diretório, adiciona em negrito e inclui filhos
        html += f"{indent}<b>{no.nome}</b> ({len(no.filhos)} filhos, {no.tamanho} bytes)<br>\n"
        for filho in no.filhos:  # Para cada filho, adiciona HTML recursivamente
            html += exportar_html(filho, nivel + 1)
    return html  # Retorna o conteúdo HTML gerado

def salvar_html(conteudo):  # Função para salvar o conteúdo HTML em um arquivo
    with open("saida.html", "w") as f:  # Abre o arquivo de saída
        f.write("<html><body>\n" + conteudo + "</body></html>")  # Escreve o conteúdo com tags básicas
    print("Exportado para 'saida.html'.")  # Exibe mensagem de sucesso

def encontrar_maior_arquivo(no, maiores=None, max_tam=0):  # Encontra o maior arquivo na árvore
    if maiores is None:
        maiores = []  # Inicializa a lista se for a primeira chamada

    if no.eh_arquivo:  # Se for um arquivo
        if no.tamanho > max_tam:  # Se for maior que o tamanho atual
            return [no], no.tamanho  # Atualiza lista e tamanho
        elif no.tamanho == max_tam:  # Se for do mesmo tamanho
            maiores.append(no)  # Adiciona à lista
    else:
        for filho in no.filhos:  # Se for diretório, percorre filhos recursivamente
            maiores, max_tam = encontrar_maior_arquivo(filho, maiores, max_tam)
    return maiores, max_tam  # Retorna os maiores arquivos e seu tamanho

def arquivos_maiores_que(no, limite):  # Encontra arquivos com tamanho acima de um limite
    resultados = []  # Lista de arquivos encontrados

    def buscar(n):  # Função recursiva interna
        if n.eh_arquivo and n.tamanho > limite:  # Se for arquivo e tamanho maior que limite
            resultados.append(n)  # Adiciona à lista
        elif not n.eh_arquivo:  # Se for diretório
            for f in n.filhos:  # Busca nos filhos
                buscar(f)
    buscar(no)  # Inicia busca a partir do nó raiz
    return resultados  # Retorna arquivos encontrados

def pasta_com_mais_arquivos(no): # Encontra a pasta com mais arquivos
    melhor_pasta = None # Inicializa a melhor pasta como None
    max_qtd = -1 # Inicializa a quantidade máxima como -1

    def buscar(n): # Função recursiva para buscar a pasta com mais arquivos
        nonlocal melhor_pasta, max_qtd # Usa variáveis externas para armazenar a melhor pasta e a quantidade máxima
        if not n.eh_arquivo: # Se não for um arquivo
            qtd = sum(1 for f in n.filhos if f.eh_arquivo or f.filhos) # Conta a quantidade de arquivos diretos ou subdiretórios
            if qtd > max_qtd: # Se a quantidade for maior que a máxima encontrada
                melhor_pasta = n # Atualiza a melhor pasta
                max_qtd = qtd # Atualiza a quantidade máxima
            for f in n.filhos: # Busca recursivamente nos filhos
                buscar(f)

    buscar(no) # Inicia a busca a partir do nó raiz
    return melhor_pasta, max_qtd # Retorna a melhor pasta e a quantidade de arquivos diretos

def arquivos_por_extensao(no, extensao): # Encontra arquivos com uma extensão específica
    encontrados = [] # Lista de arquivos encontrados

    def buscar(n): # Função recursiva para buscar arquivos por extensão
        if n.eh_arquivo and n.nome.endswith(extensao): # Se for um arquivo e a extensão bater   
            encontrados.append(n) # Adiciona à lista
        elif not n.eh_arquivo: # Se for um diretório
            for f in n.filhos: # Busca recursivamente nos filhos
                buscar(f)

    buscar(no) # Inicia a busca a partir do nó raiz
    return encontrados # Retorna os arquivos encontrados com a extensão especificada

def pastas_vazias(no):  # Encontra diretórios que não contêm nenhum arquivo ou pasta
    vazias = []  # Lista de pastas vazias

    def buscar(n):  # Função recursiva
        if not n.eh_arquivo:  # Se não for arquivo
            if len(n.filhos) == 0:  # Se não tem filhos, é vazia
                vazias.append(n)  # Adiciona à lista
            else:  # Se tem filhos, continua buscando
                for f in n.filhos:
                    buscar(f)

    buscar(no)  # Inicia busca
    return vazias  # Retorna pastas vazias

# === INÍCIO DO PROGRAMA ===

# Verifica se o caminho foi passado via linha de comando
if len(sys.argv) > 1:
    caminho_raiz = sys.argv[1]  # Usa o caminho passado pelo usuário
else:
    caminho_raiz = "."  # Caso contrário, usa o diretório atual (ponto)

raiz = No(os.path.abspath(caminho_raiz))  # Cria o nó raiz da árvore com o caminho absoluto

# === MENU INTERATIVO ===
while True:
    print("\n=== MENU ===")
    print("1 - Exibir árvore")
    print("2 - Exportar para HTML")
    print("3 - Pesquisar")
    print("3.1 - Maior arquivo")
    print("3.2 - Arquivos maiores que N bytes")
    print("3.3 - Pasta com mais arquivos diretos")
    print("3.4 - Arquivos por extensão")
    print("3.5 - Pastas vazias")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1": # Exibe a árvore de diretórios
        exibir_arvore(raiz)
    elif opcao == "2": # Exporta a árvore para HTML
        html = exportar_html(raiz) # Gera o conteúdo HTML da árvore
        salvar_html(html) # Salva o conteúdo HTML em um arquivo
    elif opcao == "3.1": # Encontra o maior arquivo na árvore
        maiores, tamanho = encontrar_maior_arquivo(raiz) # Encontra os maiores arquivos
        print("\nMaior(es) arquivo(s):") # Exibe os maiores arquivos encontrados
        for arq in maiores: # Exibe cada arquivo encontrado
            print(f"{arq.caminho} ({arq.tamanho} bytes)") # Exibe o caminho e tamanho do arquivo
    elif opcao == "3.2": # Encontra arquivos maiores que um valor N em bytes
        try:
            n = int(input("Digite o valor N em bytes: ")) # Solicita o valor N ao usuário
            encontrados = arquivos_maiores_que(raiz, n) # Encontra os arquivos maiores que N bytes
            print(f"\nArquivos maiores que {n} bytes:") # Exibe os arquivos encontrados
            for a in encontrados: # Exibe cada arquivo encontrado
                print(f"{a.caminho} ({a.tamanho} bytes)") # Exibe o caminho e tamanho do arquivo
        except ValueError: # Se o valor N não for um número válido
            print("Valor inválido.") # Exibe mensagem de erro
    elif opcao == "3.3": # Encontra a pasta com mais arquivos diretos
        pasta, qtd = pasta_com_mais_arquivos(raiz)
        if pasta: # Se encontrou uma pasta
            print(f"\nPasta com mais arquivos: {pasta.caminho} ({qtd} filhos)") # Exibe o caminho da pasta e a quantidade de arquivos diretos
    elif opcao == "3.4": # Encontra arquivos por extensão
        ext = input("Digite a extensão (ex: .txt): ").strip() # Solicita a extensão ao usuário
        encontrados = arquivos_por_extensao(raiz, ext) # Encontra os arquivos com a extensão especificada
        print(f"\nArquivos com extensão '{ext}':") # Exibe os arquivos encontrados
        for a in encontrados: # Exibe cada arquivo encontrado
            print(f"{a.caminho} ({a.tamanho} bytes)") # Exibe o caminho e tamanho do arquivo
    elif opcao == "3.5": # Encontra pastas vazias
        vazias = pastas_vazias(raiz)
        print("\nPastas vazias:") # Exibe as pastas vazias encontradas
        for p in vazias: # Exibe cada pasta vazia encontrada
            print(p.caminho) # Exibe o caminho da pasta vazia
    elif opcao == "0": # Encerra o programa
        break
    else: # Se a opção for inválida
        print("Opção inválida.")
