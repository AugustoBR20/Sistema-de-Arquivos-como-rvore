Trabalho Final - Estrutura de dados II

Alunos: João Paulo Gatto de Oliveira, Matheus Possel e Augusto Rosa

Linguagem Escolhida: Python

=========================================================================================================================================================================================================================================================================

{Gerenciador de Sistema de Arquivos com Árvores Gerais}

Funcionalidades Obrigatórias:
Carregamento Inicial:
Ao iniciar, o programa deve carregar a estrutura real do sistema de arquivos para uma árvore na memória.
Se um caminho for passado como argumento de linha de comando, será utilizado como ponto inicial. Caso nenhum argumento seja fornecido, a pasta atual será utilizada como diretório inicial.
Considerar apenas arquivos regulares e pastas (ignorar links, dispositivos, sockets, etc.).


Menu Interativo:
Após o carregamento inicial, exibir um menu interativo com as seguintes opções:
1. Exibir a árvore completa:
Exibir a árvore com indentação, refletindo a hierarquia.
Para arquivos exibir:
Nome do arquivo.
Tamanho em bytes.
Para pastas exibir:
Nome da pasta.
Quantidade de filhos (arquivos e subpastas diretos).
Tamanho total acumulado dos arquivos contidos (considerando recursivamente todos os subpastas).
2. Exportar a árvore para HTML:
Gerar um arquivo HTML mostrando a estrutura da árvore, mantendo o formato indentado.
Arquivos e pastas devem apresentar as mesmas informações do item 1.


3. Pesquisar:
3.1 Maior arquivo:
Exibir o(s) nome(s) completo(s) (com caminho) e tamanho do(s) maior(es) arquivo(s) encontrado(s). Em caso de empate, listar todos os arquivos com tamanho máximo.
3.2 Todos os arquivos com mais do que N bytes:
Solicitar um valor N ao usuário e listar todos os arquivos com tamanho maior do que esse valor, mostrando o caminho completo e o tamanho.
3.3 Pasta com mais arquivos:
Exibir o caminho completo da pasta que contém mais arquivos diretamente (não recursivo), indicando a quantidade de arquivos.
3.4 Arquivos por extensão:
Solicitar ao usuário uma extensão e listar todos os arquivos que possuem essa extensão.
3.5 Pastas vazias:
Listar todas as pastas sem arquivos ou subpastas.
