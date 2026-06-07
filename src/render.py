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
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #f9f9f9;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}
header h1 {{
  margin: 0 0 4px 0;
  font-size: 20px;
}}
header p {{
  margin: 2px 0;
  font-size