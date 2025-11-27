import os
import html
import json
from src.utils import detectar_acordes

def carregar_config():
    """Carrega o config.json da raiz do projeto"""
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(raiz, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"dominante": "destro"}  # padrão se não existir


def gerar_cabecalho_html(titulo, artista, ritmo, acordes, pasta_imagens):
    config = carregar_config()
    dominante = config.get("dominante", "destro").lower()

    imgs = []
    for ac in acordes:
        # Exemplo: acordes/destro/C.png ou acordes/canhoto/C.png
        path = os.path.join(pasta_imagens, dominante, f"{ac}.png")
        if os.path.exists(path):
            imgs.append(
                f'<figure style="display:inline-block;margin:8px;text-align:center">'
                f'<img src="../acordes/{dominante}/{ac}.png" alt="{ac} ({dominante})" width="90">'
                f'<figcaption>{ac}</figcaption></figure>'
            )
        else:
            imgs.append(
                f'<span style="display:inline-block;margin:8px;border:1px dashed #aaa;padding:6px">'
                f'{ac} ({dominante}, sem imagem)</span>'
            )

    return f"""
<header>
  <h1 style="margin-bottom:4px">{titulo}</h1>
  <p style="color:#555;margin-top:0"><strong>Artista:</strong> {artista}</p>
  <p style="color:#555;margin-top:0"><strong>Ritmo:</strong> {ritmo}</p>
  <p style="color:#555;margin-top:0"><strong>Versão:</strong> {dominante.capitalize()}</p>
  <div>{''.join(imgs)}</div>
</header>
<hr>
"""


def render_html(musica_struct, pasta_imagens):
    titulo = musica_struct["titulo"]
    artista = musica_struct["artista"]
    ritmo = musica_struct["ritmo"]
    letra = musica_struct["letra"]

    acordes = musica_struct["acordes_listados"] or detectar_acordes(letra)

    # Escapa HTML e preserva espaços
    letra_html = html.escape(letra).replace(" ", "&nbsp;")
    corpo = f"<div class='letra'>{letra_html}</div>"

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
  margin-bottom: 20px;
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
footer {{
  text-align: center;
  font-size: 12px;
  color: #888;
  margin-top: 40px;
}}
</style>
</head>
<body>
{gerar_cabecalho_html(titulo, artista, ritmo, acordes, pasta_imagens)}
{corpo}
<footer>
  Criado por Emanuel Robert Costa – Songbook pessoal<br>
  Gerado em 27/11/2025
</footer>
</body>
</html>
"""
    return base