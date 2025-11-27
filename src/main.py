import os

from src.parser import parse_musica
from src.render import render_html
from src.validador import validar_musica
import json

def carregar_config():
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(raiz, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"owner": "Songbook"}

def carregar_arquivo_caminho(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def salvar_arquivo(path, conteudo):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(conteudo)

def gerar_index(pasta_saidas):
    config = carregar_config()
    owner = config.get("owner", "Songbook")
    
    links = []
    for nome_arquivo in sorted(os.listdir(pasta_saidas)):
        if nome_arquivo.endswith(".html"):
            base = os.path.splitext(nome_arquivo)[0]
            if " - " in base:
                artista, titulo = base.split(" - ", 1)
                texto_link = f"{titulo} – {artista}"
            else:
                texto_link = base
            links.append(f'<li><a href="saidas/{nome_arquivo}">{texto_link}</a></li>')

    conteudo = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Songbook do {owner}</title>
  <style>
    body {{
      font-family: sans-serif;
      padding: 40px;
      background: #fff;
    }}
    h1 {{
      margin-bottom: 20px;
    }}
    #search {{
      width: 100%;
      padding: 10px;
      margin-bottom: 20px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 6px;
    }}
    ul {{
      list-style: none;
      padding: 0;
    }}
    li {{
      margin-bottom: 10px;
    }}
    a {{
      text-decoration: none;
      color: #2c3e50;
      font-size: 18px;
    }}
    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <h1>🎶 Songbook do {owner}</h1>
  
  <!-- Caixa de busca -->
  <input type="text" id="search" placeholder="Digite para buscar música ou artista...">

  <ul id="songList">
    {''.join(links)}
  </ul>

  <script>
    const searchInput = document.getElementById('search');
    const songList = document.getElementById('songList');

    searchInput.addEventListener('keyup', function() {{
      const filter = searchInput.value.toLowerCase();
      const items = songList.getElementsByTagName('li');
      for (let i = 0; i < items.length; i++) {{
        const text = items[i].textContent.toLowerCase();
        items[i].style.display = text.includes(filter) ? '' : 'none';
      }}
    }});
  </script>
</body>
</html>
"""
    index_path = os.path.join(os.path.dirname(pasta_saidas), "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Índice gerado com busca: {index_path}")

def processar_todas_as_musicas():
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pasta_musicas = os.path.join(raiz, "musicas")
    pasta_acordes = os.path.join(raiz, "acordes")
    pasta_saidas = os.path.join(raiz, "saidas")

    for nome_arquivo_md in os.listdir(pasta_musicas):
        if not nome_arquivo_md.endswith(".md"):
            continue
        print(f"\nProcessando '{nome_arquivo_md}'...")

        md_path = os.path.join(pasta_musicas, nome_arquivo_md)
        md_text = carregar_arquivo_caminho(md_path)
        
        erros = validar_musica(md_text, nome_arquivo_md)
        if erros:
            print("⛔ Arquivo não será processado até que os erros sejam corrigidos.")
            return

        musica_struct = parse_musica(md_text)
        html = render_html(musica_struct, pasta_acordes)

        # Nome do arquivo: Artista - Título.html
        saida_html_path = os.path.join(
            pasta_saidas,
            f"{musica_struct['artista']} - {musica_struct['titulo']}.html"
        )
        salvar_arquivo(saida_html_path, html)
        print(f"✅ Arquivo gerado: {saida_html_path}")

    # Gera o índice automaticamente com busca
    gerar_index(pasta_saidas)

if __name__ == "__main__":
    processar_todas_as_musicas()