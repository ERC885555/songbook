def validar_musica(md_text: str, nome_arquivo: str = "") -> list:
    erros = []
    linhas = md_text.splitlines()

    tem_titulo = any(ln.strip().lower().startswith("música:") for ln in linhas)
    tem_artista = any(ln.strip().lower().startswith("artista:") for ln in linhas)
    tem_ritmo = any(ln.strip().lower().startswith("ritmo:") for ln in linhas)
    tem_acordes = any(ln.strip().lower() == "[acordes]" for ln in linhas)
    tem_letra = any(ln.strip().lower() == "[letra]" for ln in linhas)

    if not tem_titulo:
        erros.append("Falta o título (linha com 'Música:').")
    if not tem_artista:
        erros.append("Falta o artista (linha com 'Artista:').")
    if not tem_ritmo:
        erros.append("Falta o ritmo (linha com 'Ritmo:').")
    if not tem_acordes:
        erros.append("Falta a seção [Acordes].")
    if not tem_letra:
        erros.append("Falta a seção [Letra].")

    if erros:
        print(f"\n⚠️ Erros encontrados em '{nome_arquivo}':")
        for e in erros:
            print(f"  - {e}")
    else:
        print(f"✅ '{nome_arquivo}' está formatado corretamente.")

    return erros