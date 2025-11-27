def parse_musica(md_text: str):
    """
    Lê o conteúdo da música em markdown simples e devolve um dicionário estruturado.
    Campos: titulo, artista, ritmo, acordes_listados, letra
    """
    linhas = md_text.splitlines()
    titulo = ""
    artista = ""
    ritmo = ""
    acordes_listados = []
    letra_lines = []
    sec = None

    for ln in linhas:
        s = ln.strip()

        # Agora o título só é aceito com "Música:"
        if s.lower().startswith("música:"):
            titulo = s.split(":", 1)[1].strip()
            continue

        if s.lower().startswith("artista:"):
            artista = s.split(":", 1)[1].strip()
            continue

        if s.lower().startswith("ritmo:"):
            ritmo = s.split(":", 1)[1].strip()
            continue

        if s == "[Acordes]":
            sec = "acordes"
            continue
        if s == "[Letra]":
            sec = "letra"
            continue

        if sec == "acordes":
            # separa por vírgula
            acordes_listados = [a.strip() for a in s.split(",") if a.strip()]
        elif sec == "letra":
            letra_lines.append(ln)

    letra = "\n".join(letra_lines).strip()
    return {
        "titulo": titulo,
        "artista": artista,
        "ritmo": ritmo,
        "acordes_listados": acordes_listados,
        "letra": letra
    }