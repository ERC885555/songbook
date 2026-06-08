import os
import json

from src.parser import parse_musica
from src.render import render_html
from src.validador import validar_musica

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
    
    musicas_info = []
    for nome_arquivo in os.listdir(pasta_saidas):
        if nome_arquivo.endswith(".html"):
            base = os.path.splitext(nome_arquivo)[0]
            if " - " in base:
                artista, titulo = base.split(" - ", 1)
            else:
                artista, titulo = "Desconhecido", base
            musicas_info.append((titulo, artista, nome_arquivo))

    # Ordena inicialmente por título
    musicas_info.sort(key=lambda x: x[0].lower())

    linhas = []
    for titulo, artista, nome_arquivo in musicas_info:
        linhas.append(
            f"<tr><td>{titulo}</td><td>{artista}</td><td><a href='saidas/{nome_arquivo}'>Abrir</a></td></tr>"
        )

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
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      border: 1px solid #ccc;
      padding: 8px;
      text-align: left;
    }}
    th {{
      background-color: #f2f2f2;
      cursor: pointer;
    }}
    tr:hover {{
      background-color: #f9f9f9;
    }}
  </style>
</head>
<body>
  <h1>🎶 Songbook do {owner}</h1>

  <!-- Caixa de busca -->
  <input type="text" id="search" placeholder="Digite para buscar música ou artista...">

  <table id="songTable">
    <thead>
      <tr>
        <th onclick="sortTable(0)">Música ⬍</th>
        <th onclick="sortTable(1)">Artista ⬍</th>
        <th>Ação</th>
      </tr>
    </thead>
    <tbody>
      {''.join(linhas)}
    </tbody>
  </table>

  <script>
    const searchInput = document.getElementById('search');
    const songTable = document.getElementById('songTable');
    const rows = songTable.getElementsByTagName('tr');

    searchInput.addEventListener('keyup', function() {{
      const filter = searchInput.value.toLowerCase();
      for (let i = 1; i < rows.length; i++) {{
        const text = rows[i].textContent.toLowerCase();
        rows[i].style.display = text.includes(filter) ? '' : 'none';
      }}
    }});

    function sortTable(n) {{
      let table = document.getElementById("songTable");
      let switching = true;
      let dir = "asc";
      let switchcount = 0;

      while (switching) {{
        switching = false;
        let rows = table.rows;
        for (let i = 1; i < (rows.length - 1); i++) {{
          let shouldSwitch = false;
          let x = rows[i].getElementsByTagName("TD")[n];
          let y = rows[i + 1].getElementsByTagName("TD")[n];
          if (dir === "asc" && x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {{
            shouldSwitch = true;
            break;
          }}
          if (dir === "desc" && x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {{
            shouldSwitch = true;
            break;
          }}
        }}
        if (shouldSwitch) {{
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount++;
        }} else {{
          if (switchcount === 0 && dir === "asc") {{
            dir = "desc";
            switching = true;
          }}
        }}
      }}
    }}
  </script>
</body>
</html>
"""
    index_path = os.path.join(os.path.dirname(pasta_saidas), "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Índice gerado com busca e ordenação: {index_path}")

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
        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        
        erros = validar_musica(md_text, nome_arquivo_md)
        if erros:
            print("⛔ Arquivo não será processado até que os erros sejam corrigidos.")
            return

        musica_struct = parse_musica(md_text)
        html = render_html(musica_struct, pasta_acordes)

        saida_html_path = os.path.join(
            pasta_saidas,
            f"{musica_struct['artista']} - {musica_struct['titulo']}.html"
        )
        salvar_arquivo(saida_html_path, html)
        print(f"✅ Arquivo gerado: {saida_html_path}")

    gerar_index(pasta_saidas)

if __name__ == "__main__":
    processar_todas_as_musicas()
