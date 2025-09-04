import re

def extrair_valores_regex(texto):
    
    rgx = r"^(.*?): Última compra em (\d{2}/\d{2}/\d{4}) \((\d+) dias atrás\) -> (\w+)"
    resultado = re.match(rgx, texto)
    
    if resultado:
        return resultado.groups()
    return None