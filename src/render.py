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
  <h1>{titulo}</h1>
  <p><strong>Artista:</strong> {artista}</p>
  <p><strong>Ritmo:</strong> {ritmo}</p>
  <p><strong>Versão:</strong> <span id="versao-label">{dominante.capitalize()}</span></p>
  <div class="acordes">{''.join(imgs)}</div>
  <div class="invert-controls">
    <button onclick="toggleDominante()" class="invert-btn">
      🔄 Alternar Destro/Canhoto
    </button>
  </div>
</header>
<div class="zoom-controls">
  <button onclick="zoomIn()" class="zoom-btn">🔍➕ Zoom In</button>
  <button onclick="zoomOut()" class="zoom-btn">🔍➖ Zoom Out</button>
</div>
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
  color: #555;
}}
.invert-controls {{
  margin-bottom: 16px;
}}
.invert-btn {{
  background-color: #FF9800;
  color: white;
  border: none;
  padding: 8px 14px;
  font-size: 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}}
.invert-btn:hover {{
  background-color: #e68900;
  transform: scale(1.05);
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
button {{
  font-size: 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}}
.layout-toggle, .zoom-btn {{
  background-color: #0078D4;
  color: white;
  border: none;
  padding: 10px 16px;
  margin-bottom: 12px;
  margin-right: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}
.layout-toggle:hover, .zoom-btn:hover {{
  background-color: #005fa3;
  transform: scale(1.05);
}}
.letra {{
  column-count: 2;
  column-gap: 40px;
  column-rule: 2px solid #000;
  font-family: monospace;
  font-size: 16px;
  line-height: 1.4;
  white-space: pre-wrap;
}}
.one-column {{
  column-count: 1;
}}
footer {{
  text-align: center;
  font-size: 12px;
  color: #888;
  margin-top: 40px;
}}
.zoom-controls {{
  margin-bottom: 16px;
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

let currentSize = 80;

function zoomIn() {{
  currentSize += 10;
  updateSize();
}}

function zoomOut() {{
  if (currentSize > 40) {{
    currentSize -= 10;
    updateSize();
  }}
}}

function updateSize() {{
  const imgs = document.querySelectorAll('.acordes img');
  imgs.forEach(img => {{
    img.style.height = currentSize + 'px';
  }});
}}

let dominanteAtual = "destro";

function toggleDominante() {{
  dominanteAtual = (dominanteAtual === "destro") ? "canhoto" : "destro";
  const imgs = document.querySelectorAll('.acordes img');
  imgs.forEach(img => {{
    const nomeAcorde = img.alt.split(" ")[0];
    img.src = "../acordes/" + dominanteAtual + "/" + nomeAcorde + ".png";
    img.alt = nomeAcorde + " (" + dominanteAtual + ")";
  }});

  const versaoLabel = document.getElementById("versao-label");
  versaoLabel.textContent = dominanteAtual.charAt(0).toUpperCase() + dominanteAtual.slice(1);
}}
</script>
</body>
</html>"""
    return base