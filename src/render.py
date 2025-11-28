import os
import html
import json

def carregar_config():
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(raiz, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"dominante": "destro"}

def gerar_cabecalho_html(titulo, artista, ritmo, acordes, pasta_imagens):
    config = carregar_config()
    dominante = config.get("dominante", "destro").lower()

    imgs = []
    for ac in acordes:
        path = os.path.join(pasta_imagens, dominante, f"{ac}.png")
        if os.path.exists(path):
            imgs.append(
                f'<figure><img src="../acordes/{dominante}/{ac}.png" alt="{ac} ({dominante})"><figcaption>{ac}</figcaption></figure>'
            )
        else:
            imgs.append(
                f'<span class="acorde-faltando">{ac} ({dominante}, sem imagem)</span>'
            )

    return f"""
<header>
  <h1 style="margin-bottom:4px">{titulo}</h1>
  <p style="color:#555;margin-top:0"><strong>Artista:</strong> {artista}</p>
  <p style="color:#555;margin-top:0"><strong>Ritmo:</strong> {ritmo}</p>
  <p style="color:#555;margin-top:0"><strong>Versão:</strong> {dominante.capitalize()}</p>
  <div class="acordes">{''.join(imgs)}</div>
</header>
<hr>
"""

def render_html(musica_struct, pasta_imagens):
    titulo = musica_struct["titulo"]
    artista = musica_struct["artista"]
    ritmo = musica_struct["ritmo"]
    letra = musica_struct["letra"]
    acordes = musica_struct.get("acordes_listados", [])

    letra_html = html.escape(letra).replace(" ", "&nbsp;")
    corpo = f"<div id='song' class='letra'>{letra_html}</div>"

    base = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{titulo}</title>
<style>
body {{
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  padding: 24px;
}}
hr {{
  margin: 20px 0;
}}
header {{
  background-color: #f9f9f9;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
}}
header h1 {{
  margin: 0 0 4px 0;
  font-size: 20px;
}}
header p {{
  margin: 2px 0;
  font-size: 14px;
}}
.acordes {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: start;
  margin-top: 8px;
  margin-bottom: 12px;
}}
.acordes figure {{
  margin: 0;
  text-align: center;
  width: 80px;
}}
.acordes img {{
  height: 80px;
  object-fit: contain;
}}
.acorde-faltando {{
  display: inline-block;
  margin: 8px;
  border: 1px dashed #aaa;
  padding: 6px;
  font-size: 14px;
  color: #555;
}}
.layout-toggle {{
  background-color: #0078D4;
  color: white;
  border: none;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}
.layout-toggle:hover {{
  background-color: #005fa3;
  transform: scale(1.03);
}}
.letra {{
  column-count: 2;   /* padrão: 2 blocos */
  column-gap: 40px;
  column-rule: 2px solid #000;
  font-family: monospace;
  font-size: 16px;
  line-height: 1.4;
  white-space: pre-wrap;
}}
.one-column {{
  column-count: 1;   /* alterna para 1 bloco */
}}
footer {{
  text-align: center;
  font-size: 12px;
  color: #888;
  margin-top: 40px;
}}
@media print {{
  body {{
    margin: 5mm;
  }}
  header {{
    margin-bottom: 8px;
    padding: 6px;
  }}
  .letra {{
    column-gap: 24px;
  }}
}}
</style>
</head>
<body>
{gerar_cabecalho_html(titulo, artista, ritmo, acordes, pasta_imagens)}

<!-- Botão estilizado para alternar layout -->
<button onclick="toggleColumns()" class="layout-toggle">
  🎛️ Alternar entre 1 ou 2 blocos
</button>

{corpo}

<footer>
  Criado por Emanuel Robert Costa – Songbook pessoal<br>
  Gerado em 27/11/2025
</footer>

<script>
function toggleColumns() {{
  const song = document.getElementById('song');
  song.classList.toggle('one-column');
}}
</script>
</body>
</html>"""
    return base