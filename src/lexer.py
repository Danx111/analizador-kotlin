"""
Analizador léxico para un subconjunto de Kotlin usando PLY (ply.lex).

ESTRUCTURA BASE COMPARTIDA
--------------------------
Cada integrante trabaja SOLO dentro de su sección (marcada con ===== NOMBRE =====)
para evitar conflictos al hacer merge entre ramas:

    1. Palabras reservadas  -> reserved_<nombre>
    2. Tokens adicionales   -> tokens_<nombre>
    3. Reglas simples       -> t_TOKEN = r'...'      (strings)
    4. Reglas con acción    -> def t_TOKEN(t): ...   (funciones)

Notas de PLY:
    - Las reglas definidas como FUNCIÓN se prueban en el orden en que aparecen.
    - Las reglas definidas como STRING se ordenan por longitud de regex
      (de mayor a menor), así '==' se prueba antes que '='.
    - Las funciones siempre se prueban ANTES que los strings.
    - Las palabras reservadas NO necesitan regla propia: t_ID las detecta
      consultando el diccionario `reserved`.

Uso:
    python src/lexico/lexer.py <archivo.kt> <usuario_github>
    Ejemplo: python src/lexico/lexer.py algoritmos/algoritmo_alan.kt alan-am
"""

import sys
from datetime import datetime
from pathlib import Path

import ply.lex as lex

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_LOGS = RAIZ_PROYECTO / "logs"


# =============================================================================
# 1. PALABRAS RESERVADAS
# =============================================================================

# ===== Mateo Andrade =====
reserved_mateo = {
    "var": "VAR",
    "fun": "FUN",
    "return": "RETURN",
    "if": "IF",
    "else": "ELSE",
    "listOf": "LISTOF",
    "mutableListOf": "MUTABLELISTOF",
    "println": "PRINTLN",
    "print": "PRINT",
    "readLine": "READLINE",
    "readln": "READLN",
    "Int": "TIPO_INT",
    "Long": "TIPO_LONG",
    "Double": "TIPO_DOUBLE",
    "Float": "TIPO_FLOAT",
    "List": "TIPO_LIST",
    "MutableList": "TIPO_MUTABLELIST",
}

# ===== Alan Aguilar =====
reserved_alan = {
    "val": "VAL",       
    "when": "WHEN",     # switch
    "for": "FOR",       
    "in": "IN",         # for (x in coleccion)
    "while": "WHILE",  
    "do": "DO",         
    "true": "TRUE",
    "false": "FALSE",
    "mapOf": "MAPOF",
    "mutableMapOf": "MUTABLEMAPOF",
    "to": "TO",        # "clave" to valor
}

# ===== Daniela Espinoza =====
reserved_daniela = {
    'const' : 'CONST',
    'String' : 'TIPO_STRING',
    'Boolean' : 'TIPO_BOOLEAN',
    'null': 'NULL',
    'true': 'TRUE',
    'false': 'FALSE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'class': 'CLASS',
    'Set': 'TIPO_SET',
    'MutableSet': 'TIPO_MUTABLESET',
    'setOf': 'SETOF',
    'mutableSetOf': 'MUTABLESETOF',
    'is': 'IS',
    'as': 'AS',
}

reserved = {**reserved_mateo, **reserved_alan, **reserved_daniela}


# =============================================================================
# 2. LISTA DE TOKENS (no incluir aquí las palabras reservadas)
# =============================================================================

tokens_base = [
    "ID",
]

# ===== Mateo Andrade =====
tokens_mateo = [
    "ENTERO",
    "ENTERO_LARGO",
    "DECIMAL",
    "FLOTANTE",
    "MAS",
    "MENOS",
    "POR",
    "DIVIDIDO",
    "MODULO",
    "ASIGNAR",
    "MAS_ASIGNAR",
    "MENOS_ASIGNAR",
    "POR_ASIGNAR",
    "DIVIDIDO_ASIGNAR",
    "MODULO_ASIGNAR",
    "RANGO",
    "LLAVEIZQ",
    "LLAVEDER",
]

# ===== Alan Aguilar =====
tokens_alan = [
    "CHAR",
    "INCREMENTO", "DECREMENTO",
    "IGUAL", "DIFERENTE", "MENOR", "MAYOR", "MENORIGUAL", "MAYORIGUAL",
    # Lógicos
    "AND", "OR", "NOT",
    # Delimitadores
    "LPAREN", "RPAREN", "CORCHETEIZQ", "CORCHETEDER", "COMA",
]

# ===== Daniela Espinoza =====
tokens_daniela = [
    'STRING_LITERAL',
    'CHAR_LITERAL',
    'QUESTION',
    'SAFE_CALL',        # ?.
    'ELVIS',            # ?:
    'NOT_NULL_ASSERT',  # !!
    'ARROW',            # ->
    'NEWLINE',
    'COLON',            # : 
    'SEMICOLON',        # ; 
    'DOT',
]

tokens = (
    tokens_base
    + tokens_mateo
    + tokens_alan
    + tokens_daniela
    + list(dict.fromkeys(reserved.values()))
)


# =============================================================================
# 3. REGLAS SIMPLES (strings)
# =============================================================================

# ===== Mateo Andrade =====
t_MAS = r"\+"
t_MENOS = r"-"
t_POR = r"\*"
t_DIVIDIDO = r"/"
t_MODULO = r"%"

t_ASIGNAR = r"="
t_MAS_ASIGNAR = r"\+="
t_MENOS_ASIGNAR = r"-="
t_POR_ASIGNAR = r"\*="
t_DIVIDIDO_ASIGNAR = r"/="
t_MODULO_ASIGNAR = r"%="

t_RANGO = r"\.\."

t_LLAVEIZQ = r"\{"
t_LLAVEDER = r"\}"
# ===== Fin Mateo Andrade =====

# ===== Alan Aguilar =====
# Char: un solo carácter o una secuencia de escape entre comillas simples
# Ejemplos: 'a', '7', '\n', '\''
t_CHAR = r"'([^'\\\n]|\\[tbnr'\"\\$])'"

t_INCREMENTO = r"\+\+"
t_DECREMENTO = r"--"

# Relacionales 
t_IGUAL = r"=="
t_DIFERENTE = r"!="
t_MENORIGUAL = r"<="
t_MAYORIGUAL = r">="
t_MENOR = r"<"
t_MAYOR = r">"

# Lógicos
t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"

# Delimitadores
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_CORCHETEIZQ = r"\["
t_CORCHETEDER = r"\]"
t_COMA = r","


# ===== Daniela Espinoza =====
t_ELVIS = r'\?:'
t_SAFE_CALL = r'\?\.'
t_QUESTION = r'\?' 
t_NOT_NULL_ASSERT = r'!!'
t_ARROW = r'->'

t_COLON = r':'
t_SEMICOLON = r';'
t_DOT  = r'\.'

# =============================================================================
# 4. REGLAS CON ACCIÓN (funciones) — el orden importa
# =============================================================================

# ===== Mateo Andrade =====
def t_COMENTARIO_MULTILINEA(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")


def t_COMENTARIO_SIN_CERRAR(t):
    r"/\*(.|\n)*"
    t.lexer.errores.append(f"Error léxico: comentario sin cerrar en la línea {t.lineno}")
    t.lexer.lineno += t.value.count("\n")


def t_COMENTARIO_LINEA(t):
    r"//[^\n]*"
    pass


def t_FLOTANTE(t):
    r"\d+(\.\d+)?[fF]"
    t.value = float(t.value[:-1])
    return t


def t_DECIMAL(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_ENTERO_LARGO(t):
    r"\d[\d_]*L"
    t.value = int(t.value[:-1].replace("_", ""))
    return t


def t_ENTERO(t):
    r"\d[\d_]*"
    t.value = int(t.value.replace("_", ""))
    return t


# ===== Daniela Espinoza =====
def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t


# =============================================================================
# 5. REGLAS COMUNES (base compartida)
# =============================================================================

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = " \t\r"


def t_error(t):
    mensaje = (
        f"Error léxico: carácter no reconocido '{t.value[0]}' "
        f"en la línea {t.lineno}"
    )
    t.lexer.errores.append(mensaje)
    t.lexer.skip(1)


# =============================================================================
# 6. FUNCIONES DE ANÁLISIS Y LOG
# =============================================================================

def construir_lexer():
    lexer = lex.lex()
    lexer.errores = []
    return lexer


def analizar(codigo):
    """Devuelve (tokens, errores) del código fuente recibido."""
    lexer = construir_lexer()
    lexer.input(codigo)
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_encontrados.append(tok)
    return tokens_encontrados, lexer.errores


def generar_log(usuario, tokens_encontrados, errores, archivo_fuente=""):
    """Guarda el log con el formato lexico-usuario-ddmmaaaa-HHhMM.txt."""
    CARPETA_LOGS.mkdir(exist_ok=True)
    fecha = datetime.now().strftime("%d%m%Y-%Hh%M")
    ruta = CARPETA_LOGS / f"lexico-{usuario}-{fecha}.txt"

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Análisis léxico - {archivo_fuente}\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now():%d/%m/%Y %H:%M:%S}\n\n")
        f.write(f"TOKENS ({len(tokens_encontrados)})\n")
        for tok in tokens_encontrados:
            f.write(f"Línea {tok.lineno}: {tok.type} -> {tok.value!r}\n")
        f.write(f"\nERRORES ({len(errores)})\n")
        for err in errores:
            f.write(f"{err}\n")
    return ruta


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python src/lexico/lexer.py <archivo.kt> <usuario_github>")
        sys.exit(1)

    archivo, usuario = sys.argv[1], sys.argv[2]
    with open(archivo, encoding="utf-8-sig") as f:
        codigo = f.read()

    toks, errs = analizar(codigo)
    for tok in toks:
        print(f"Línea {tok.lineno}: {tok.type} -> {tok.value!r}")
    for err in errs:
        print(err)
    print(f"\nLog guardado en: {generar_log(usuario, toks, errs, archivo)}")
