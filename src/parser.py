"""
KotlinScope - Analizador Sintáctico (PLY yacc)
Proyecto Lenguajes de Programación - Avance 2

Integrantes:
- Mateo Andrés Andrade Domínguez
- Alan Ariel Aguilar Morocho
- Daniela Joselyne Espinoza Toala
"""

import sys
from datetime import datetime
from pathlib import Path
import ply.yacc as yacc

# Importación de la lista de tokens generada en la fase léxica
from src.lexer import tokens

# ==============================================================================
# TABLA DE PRECEDENCIA Y ASOCIATIVIDAD DE OPERADORES
# Responsable: Alan Aguilar (Aritmética) y Daniela Espinoza (Lógica/Comparación)
# ==============================================================================
precedence = (
    # Definir aquí de menor a mayor precedencia (left, right, nonassoc)
    # Ejemplos: conectores lógicos, operadores relacionales, suma/resta, mult/div, unarios
)


# ==============================================================================
# REGLAS GENERALES DEL PROGRAMA
# Responsable: Integración Conjunta
# ==============================================================================

start = "programa"


# el programa es una lista de sentencias
def p_programa(p):
    "programa : sentencias"


# las sentencias se repiten una tras otra y el punto y coma es opcional
def p_sentencias(p):
    """sentencias : sentencias sentencia
                  | sentencias SEMICOLON
                  | empty"""


# un bloque son sentencias entre llaves
def p_bloque(p):
    "bloque : LLAVEIZQ sentencias LLAVEDER"


# una expresión sola también es una sentencia, por ejemplo una llamada
def p_sentencia_expresion(p):
    "sentencia : expresion"


# los valores más simples que puede tener una expresión
def p_expresion_valor(p):
    """expresion : ID
                 | ENTERO
                 | ENTERO_LARGO
                 | DECIMAL
                 | FLOTANTE
                 | STRING_LITERAL
                 | CHAR_LITERAL
                 | TRUE
                 | FALSE
                 | NULL"""


# un tipo también puede ser el nombre de una clase
def p_tipo_nombre(p):
    "tipo : ID"


def p_empty(p):
    "empty :"


# ==============================================================================
# BLOQUE 1: MATEO ANDRADE
# - I/O (Impresión y lectura de datos)
# - Declaración inmutable con tipo inferido (val x = ...)
# - Estructuras de control: if / else if / else
# - Estructuras de datos: List / MutableList (listOf, mutableListOf)
# - Funciones con bloque, parámetros formales y tipo de retorno
# ==============================================================================

# ==============================================================================
# BLOQUE 2: ALAN AGUILAR
# - Expresiones aritméticas completas (binarias, unarias, paréntesis)
# - Declaración mutable con tipo explícito (var x: Tipo = ...)
# - Estructura de control: when (con ramas de coincidencia y else)
# - Estructuras de datos: Map / MutableMap (mapOf, mutableMapOf, 'to')
# - Funciones de expresión única (= directo) y parámetros por defecto
# ==============================================================================



# ==============================================================================
# BLOQUE 3: DANIELA ESPINOZA
# - Expresiones booleanas, operadores lógicos y comparaciones
# - Operador de rango (..)
# - Declaración de variables nullables (Tipo?) y constantes (const val)
# - Operaciones null-safety (?. , ?: , !!)
# - Estructuras de control de iteración: while y for (rango / colección)
# - Estructuras de datos: Set / MutableSet (setOf, mutableSetOf)
# - Funciones lambda ({ param -> cuerpo })
# ==============================================================================




# ==============================================================================
# MANEJO DE ERRORES SINTÁCTICOS Y GENERACIÓN DE LOGS
# ==============================================================================

CARPETA_LOGS = Path(__file__).resolve().parents[1] / "logs"
errores_sintacticos = []


# guardo cada error con el token y la línea donde pasó
def p_error(p):
    if p:
        errores_sintacticos.append(
            f"Error sintáctico: token inesperado '{p.value}' ({p.type}) en la línea {p.lineno}"
        )
    else:
        errores_sintacticos.append("Error sintáctico: el código terminó antes de tiempo")


parser = yacc.yacc(debug=False, write_tables=False)


def analizar(codigo):
    from src.lexer import construir_lexer

    errores_sintacticos.clear()
    lexer = construir_lexer()
    parser.parse(codigo, lexer=lexer)
    return lexer.errores, list(errores_sintacticos)


def generar_log_sintactico(usuario, errores_lexicos, errores, archivo_fuente=""):
    CARPETA_LOGS.mkdir(exist_ok=True)
    fecha = datetime.now().strftime("%d%m%Y-%Hh%M")
    ruta = CARPETA_LOGS / f"sintactico-{usuario}-{fecha}.txt"

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Análisis sintáctico - {archivo_fuente}\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now():%d/%m/%Y %H:%M:%S}\n\n")
        f.write(f"ERRORES LÉXICOS ({len(errores_lexicos)})\n")
        for err in errores_lexicos:
            f.write(f"{err}\n")
        f.write(f"\nERRORES SINTÁCTICOS ({len(errores)})\n")
        for err in errores:
            f.write(f"{err}\n")
        if not errores_lexicos and not errores:
            f.write("\nEl programa es sintácticamente válido.\n")
    return ruta


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python -m src.parser <archivo.kt> <usuario_github>")
        sys.exit(1)

    archivo, usuario = sys.argv[1], sys.argv[2]
    with open(archivo, encoding="utf-8-sig") as f:
        codigo = f.read()

    errores_lexicos, errores = analizar(codigo)
    for err in errores_lexicos + errores:
        print(err)
    if not errores_lexicos and not errores:
        print("El programa es sintácticamente válido.")
    print(f"\nLog guardado en: {generar_log_sintactico(usuario, errores_lexicos, errores, archivo)}")