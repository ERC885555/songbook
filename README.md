# 🎶 Songbook do Emanuel

Um songbook digital simples e automático.  
Você coloca suas músicas em formato `.md` na pasta `musicas/` e o projeto gera páginas HTML organizadas por artista e título, além de um índice com busca.

---

## 🚀 Como usar

### 1. Instalar o Python
- Certifique-se de ter o **Python 3.10+** instalado.
- Para verificar, rode:
  ```bash
  python --version

### 2. Clonar o repositório
Baixe o projeto do GitHub:
git clone https://github.com/ERC885555/songbook 
cd songbook

### 3. Criar o ambiente virtual
Rode o arquivo na pasta raiz __reset_env.bat__

Ele automaticamente apaga o ambiente virtual antigo e cria um novo com as especificações do projeto.

### 4. Instalar dependências
O arquivo __reset_env.bat__ já instala todas as dependências necessárias dentro do ambiente virtual.

### 5. Personalizar o nome do Songbook
Na raiz do projeto existe um arquivo config.json:

{
  "owner": "Emanuel",
  "dominante": "destro"
}

- Troque "owner" pelo seu nome.
- Troque "dominante" para "destro" ou "canhoto", conforme sua preferência.
- Exemplo: se o Rafael baixar o projeto e for canhoto, basta editar para:


{
  "owner": "Rafael",
  "dominante": "canhoto"
}

O título do índice será atualizado automaticamente para Songbook do Rafael e os acordes serão buscados na pasta correta.

### 6. Adicionar músicas
- Coloque seus arquivos .md dentro da pasta musicas/.
- Cada arquivo __NECESSITA__ ter metadados conforme o exemplo abaixo:

__Música:__ ``Nome da Música``
__Artista:__ ``Nome do(a) Cantor(a)``
__Ritmo:__ Padrão de batida (ex.: ``DDU UDU``)
__[Acordes]:__ Quais acordes serão exibidos no cabeçalho (ex.: ``C, Am, F, G``)

__[Letra]__
C
Primeira linha com acorde

G
Segunda linha com letra

Am
Terceira linha com acorde

F
Quarta linha com letra

## ✅ Regras claras para quem usar
- Música: obrigatório, sempre na primeira linha.
- Artista: obrigatório, logo abaixo.
- Ritmo: obrigatório, mostra a batida (ex.: DUD UDU).
- [Acordes]: bloco obrigatório, lista separada por vírgulas.
- [Letra]: bloco obrigatório, letra da música com acordes posicionados.

### 7. Gerar o songbook
No Windows, basta dar duplo clique no arquivo:
- gerar_songbook.bat → rápido, só gera os HTMLs e o índice.
- reset_env.bat → recria o ambiente virtual do zero e instala dependências (use apenas se mudar bibliotecas).

### 8. Abrir o songbook
- Após rodar o .bat, abra o arquivo index.html na raiz do projeto.
- Você verá uma lista com todas as músicas.
- Use a caixa de busca para filtrar por título ou artista

### 📂 Estrutura de pastas

songbook/

── src/              # Código fonte (parser, render, main.py, utils)
── musicas/          # Suas músicas em formato .md
── acordes/          # Diagramas de acordes (separados em destro/ e canhoto/)
── saidas/           # HTMLs gerados automaticamente
── index.html        # Índice com busca (gerado automaticamente)
── config.json       # Configuração do nome e mão dominante
── requirements.txt  # Dependências do projeto
── gerar_songbook.bat
── reset_env.bat

### 🛠️ Dicas
- Não edite manualmente os arquivos em saidas/ ou o index.html. Eles são gerados automaticamente.
- Sempre edite/adicione músicas em musicas/.
- Se algo der errado, rode o reset_env.bat para recriar o ambiente.
- O projeto funciona localmente, mas pode ser publicado no GitHub Pages ou intranet se quiser.

### 👶 Tutorial para iniciantes
- Instale Python.
- Baixe o projeto.
- Crie o venv e instale dependências.
- Personalize o nome e a mão dominante no config.json.
- Coloque suas músicas em musicas/.
- Organize os acordes em acordes/destro/ e acordes/canhoto/.
- Clique em gerar_songbook.bat.
- Abra index.html.
- Cante e seja feliz 🎤🎶