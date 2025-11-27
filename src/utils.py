import re

# Conjunto de acordes válidos (amplie conforme precisar)
BASIC_ROOTS = r"[A-G]"            # A, B, C, D, E, F, G
ACCIDENTALS = r"(?:#|b)?"         # sustenido ou bemol
QUALITIES = r"(?:m|maj7|min7|m7|7|sus2|sus4|add9|dim|aug|m6|6|9|11|13)?"  # qualidades comuns
EXTENSIONS = r"(?:/[A-G](?:#|b)?)?"  # baixarias (ex.: C/E, D/F#)

CHORD_PATTERN = re.compile(
    rf"\b{BASIC_ROOTS}{ACCIDENTALS}{QUALITIES}{EXTENSIONS}\b"
)

def detectar_acordes(texto: str):
    """Extrai acordes únicos do texto, preservando ordem de primeira ocorrência."""
    vistos = set()
    ordem = []
    for match in CHORD_PATTERN.finditer(texto):
        acorde = match.group(0)
        if acorde not in vistos:
            vistos.add(acorde)
            ordem.append(acorde)
    return ordem