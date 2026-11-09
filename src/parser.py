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
    # Daniela Espinoza (Lógica / Comparación / Rango)
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'IGUAL', 'DIFERENTE'),
    ('nonassoc', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'ELVIS'),                          # ?:
    ('nonassoc', 'RANGO'),                      # ..
    # Alan Aguilar (Aritmética binaria y unarios)
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'NOT', 'UMENOS'),                 # operadores unarios
    ('left', 'SAFE_CALL', 'NOT_NULL_ASSERT', 'INCREMENTO', 'DECREMENTO'), # postfijos
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

# agrego mis sentencias al programa
def p_sentencia_mateo(p):
    """sentencia : impresion
                 | declaracion_val
                 | reasignacion
                 | condicional
                 | funcion
                 | retorno"""


# agrego mis expresiones al programa
def p_expresion_mateo(p):
    """expresion : lectura
                 | lista
                 | acceso_lista
                 | acceso_miembro
                 | llamada_funcion"""


# imprimo con println o print
def p_impresion(p):
    """impresion : PRINTLN LPAREN expresion RPAREN
                 | PRINTLN LPAREN RPAREN
                 | PRINT LPAREN expresion RPAREN"""


# leo datos del teclado con readLine o readln
def p_lectura(p):
    """lectura : READLINE LPAREN RPAREN
               | READLN LPAREN RPAREN"""


# declaro un val sin tipo y kotlin lo deduce solo
def p_declaracion_val(p):
    """declaracion_val : VAL ID ASIGNAR expresion
                       | VAL ID ASIGNAR if_expresion"""


# cambio el valor de una variable o de una posición de la lista
def p_reasignacion(p):
    """reasignacion : ID operador_asignacion expresion
                    | acceso_lista operador_asignacion expresion"""


def p_operador_asignacion(p):
    """operador_asignacion : ASIGNAR
                           | MAS_ASIGNAR
                           | MENOS_ASIGNAR
                           | POR_ASIGNAR
                           | DIVIDIDO_ASIGNAR
                           | MODULO_ASIGNAR"""


# if, else if y else con bloques
def p_condicional(p):
    """condicional : IF LPAREN expresion RPAREN bloque
                   | IF LPAREN expresion RPAREN bloque ELSE bloque
                   | IF LPAREN expresion RPAREN bloque ELSE condicional"""


# if usado como valor, por ejemplo val letra = if (x) 'A' else 'B'
def p_if_expresion(p):
    """if_expresion : IF LPAREN expresion RPAREN expresion ELSE expresion
                    | IF LPAREN expresion RPAREN expresion ELSE if_expresion"""


# creo listas con listOf y mutableListOf
def p_lista(p):
    """lista : LISTOF LPAREN argumentos RPAREN
             | MUTABLELISTOF LPAREN argumentos RPAREN
             | LISTOF MENOR tipo MAYOR LPAREN RPAREN
             | MUTABLELISTOF MENOR tipo MAYOR LPAREN RPAREN"""


# leo una posición de la lista, por ejemplo notas[0]
def p_acceso_lista(p):
    "acceso_lista : ID CORCHETEIZQ expresion CORCHETEDER"


# uso propiedades y métodos, por ejemplo notas.size o notas.add(4)
def p_acceso_miembro(p):
    """acceso_miembro : ID DOT ID
                      | ID DOT ID LPAREN RPAREN
                      | ID DOT ID LPAREN argumentos RPAREN
                      | lectura DOT ID LPAREN RPAREN"""


# los valores separados por coma
def p_argumentos(p):
    """argumentos : expresion
                  | argumentos COMA expresion"""


# defino una función con parámetros, tipo de retorno y bloque
def p_funcion(p):
    """funcion : FUN ID LPAREN parametros RPAREN COLON tipo bloque
               | FUN ID LPAREN RPAREN COLON tipo bloque
               | FUN ID LPAREN parametros RPAREN bloque
               | FUN ID LPAREN RPAREN bloque"""


def p_parametros(p):
    """parametros : parametro
                  | parametros COMA parametro"""


# cada parámetro tiene nombre y tipo
def p_parametro(p):
    "parametro : ID COLON tipo"


# devuelvo un valor desde la función
def p_retorno(p):
    """retorno : RETURN expresion
               | RETURN"""


# llamo a una función, por ejemplo sumar(2, 3)
def p_llamada_funcion(p):
    """llamada_funcion : ID LPAREN RPAREN
                       | ID LPAREN argumentos RPAREN"""


# mis tipos: números y listas
def p_tipo_mateo(p):
    """tipo : TIPO_INT
            | TIPO_LONG
            | TIPO_DOUBLE
            | TIPO_FLOAT
            | TIPO_LIST MENOR tipo MAYOR
            | TIPO_MUTABLELIST MENOR tipo MAYOR"""




# ==============================================================================
# BLOQUE 2: ALAN AGUILAR
# - Expresiones aritméticas completas (binarias, unarias, paréntesis)
# - Declaración mutable con tipo explícito (var x: Tipo = ...)
# - Estructura de control: when (con ramas de coincidencia y else)
# - Estructuras de datos: Map / MutableMap (mapOf, mutableMapOf, 'to')
# - Funciones de expresión única (= directo) y parámetros por defecto
# ==============================================================================

# operaciones aritméticas binarias: + - * / %
# la tabla precedence decide qué se agrupa primero (a + b * c = a + (b * c))
def p_expresion_aritmetica(p):
    """expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion MODULO expresion"""


# los paréntesis cambian el orden de evaluación
def p_expresion_parentesis(p):
    "expresion : LPAREN expresion RPAREN"


# menos unario: -x, usa la precedencia de UMENOS y no la de la resta
def p_expresion_negativo(p):
    "expresion : MENOS expresion %prec UMENOS"


# incremento y decremento en 1 (postfijo): x++, x--
def p_expresion_incremento(p):
    """expresion : expresion INCREMENTO
                 | expresion DECREMENTO"""

# sentencias de Alan: declaración de variable mutable y estructura when
def p_sentencia_alan(p):
    """sentencia : declaracion_var
                 | when_stmt"""


# declaración mutable con tipo explícito (var x: Tipo = ...)
def p_declaracion_var(p):
    """declaracion_var : VAR ID COLON tipo ASIGNAR expresion
                       | VAR ID COLON tipo ASIGNAR if_expresion
                       | VAR ID COLON tipo ASIGNAR when_stmt"""


# permite usar when como expresión en asignación val (val x = when (...) { ... })
def p_declaracion_val_when(p):
    "declaracion_val : VAL ID ASIGNAR when_stmt"


# estructura de control when (con evaluación de expresiones o ramas múltiples)
def p_when_stmt(p):
    "when_stmt : WHEN LPAREN expresion RPAREN LLAVEIZQ ramas LLAVEDER"


def p_ramas(p):
    """ramas : rama
             | ramas rama
             | ramas SEMICOLON"""


def p_rama(p):
    """rama : valores ARROW cuerpo_rama
            | ELSE ARROW cuerpo_rama"""


def p_cuerpo_rama(p):
    """cuerpo_rama : sentencia
                   | bloque"""


def p_valores(p):
    """valores : expresion
               | valores COMA expresion"""


# expresiones de Alan
def p_expresion_alan(p):
    """expresion : mapa"""


# creación de mapas con mapOf y mutableMapOf
def p_mapa(p):
    """mapa : MAPOF LPAREN pares RPAREN
            | MUTABLEMAPOF LPAREN pares RPAREN
            | MAPOF LPAREN RPAREN
            | MUTABLEMAPOF LPAREN RPAREN
            | MAPOF MENOR tipo COMA tipo MAYOR LPAREN RPAREN
            | MUTABLEMAPOF MENOR tipo COMA tipo MAYOR LPAREN RPAREN"""


def p_pares(p):
    """pares : par
             | pares COMA par"""


# par clave-valor usando la palabra reservada 'to'
def p_par(p):
    "par : expresion TO expresion"


# tipos Map y MutableMap con parámetros de tipo genéricos <K, V>
def p_tipo_alan(p):
    """tipo : TIPO_MAP MENOR tipo COMA tipo MAYOR
            | TIPO_MUTABLEMAP MENOR tipo COMA tipo MAYOR"""


# funciones de expresión única (fun f(...) = expresion)
def p_funcion_expresion(p):
    """funcion : FUN ID LPAREN parametros RPAREN ASIGNAR expresion
               | FUN ID LPAREN RPAREN ASIGNAR expresion
               | FUN ID LPAREN parametros RPAREN COLON tipo ASIGNAR expresion
               | FUN ID LPAREN RPAREN COLON tipo ASIGNAR expresion"""


# parámetro formal con valor por defecto (param: Tipo = expresion)
def p_parametro_defecto(p):
    "parametro : ID COLON tipo ASIGNAR expresion"



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
# agrego mis sentencias al programa
def p_sentencia_daniela(p):
    """sentencia : declaracion_nullable
                 | declaracion_const
                 | ciclo_while
                 | ciclo_for
                 | salto"""


# agrego mis expresiones al programa
def p_expresion_daniela(p):
    """expresion : conjunto
                 | lambda_expr"""


# operadores lógicos y de comparación
def p_expresion_logica(p):
    """expresion : expresion AND expresion
                 | expresion OR expresion
                 | expresion IGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion"""


# negación lógica
def p_expresion_not(p):
    "expresion : NOT expresion"


# rango, por ejemplo 1..10
def p_expresion_rango(p):
    "expresion : expresion RANGO expresion"


# un tipo nullable es un tipo normal seguido de ?
def p_tipo_nullable(p):
    "tipo_nullable : tipo QUESTION"


# mis tipos: String, Boolean y conjuntos
def p_tipo_daniela(p):
    """tipo : TIPO_STRING
            | TIPO_BOOLEAN
            | TIPO_SET MENOR tipo MAYOR
            | TIPO_SET MENOR tipo_nullable MAYOR
            | TIPO_MUTABLESET MENOR tipo MAYOR
            | TIPO_MUTABLESET MENOR tipo_nullable MAYOR"""


# var / val con tipo nullable, por ejemplo var apodo: String? = null
def p_declaracion_nullable(p):
    """declaracion_nullable : VAR ID COLON tipo_nullable ASIGNAR expresion
                            | VAL ID COLON tipo_nullable ASIGNAR expresion
                            | VAR ID COLON tipo_nullable"""


# constantes, por ejemplo const val MAX: Int = 10
def p_declaracion_const(p):
    """declaracion_const : CONST VAL ID COLON tipo ASIGNAR expresion
                         | CONST VAL ID COLON tipo_nullable ASIGNAR expresion
                         | CONST VAL ID ASIGNAR expresion"""


# llamada segura, por ejemplo nombre?.length o nombre?.uppercase()
def p_safe_call(p):
    """expresion : expresion SAFE_CALL ID
                 | expresion SAFE_CALL ID LPAREN RPAREN
                 | expresion SAFE_CALL ID LPAREN argumentos RPAREN"""


# operador elvis, por ejemplo nombre ?: "sin nombre"
def p_elvis(p):
    "expresion : expresion ELVIS expresion"


# aserción de no nulo, por ejemplo nombre!!
def p_not_null_assert(p):
    "expresion : expresion NOT_NULL_ASSERT"


# aserción de no nulo seguida de acceso, por ejemplo nombre!!.length
def p_not_null_miembro(p):
    """expresion : expresion NOT_NULL_ASSERT DOT ID
                 | expresion NOT_NULL_ASSERT DOT ID LPAREN RPAREN
                 | expresion NOT_NULL_ASSERT DOT ID LPAREN argumentos RPAREN"""


# ------------------------------------------------------------------------------
# Ciclos: while y for (rango / colección)
# ------------------------------------------------------------------------------

# while con condición y bloque
def p_ciclo_while(p):
    "ciclo_while : WHILE LPAREN expresion RPAREN bloque"


# for sobre rango (1..10) o colección (lista): ambos son una expresion
def p_ciclo_for(p):
    "ciclo_for : FOR LPAREN ID IN expresion RPAREN bloque"


# break y continue dentro de los ciclos
def p_salto(p):
    """salto : BREAK
             | CONTINUE"""


# ------------------------------------------------------------------------------
# Set / MutableSet
# ------------------------------------------------------------------------------

# creo conjuntos con setOf y mutableSetOf
def p_conjunto(p):
    """conjunto : SETOF LPAREN RPAREN
                | SETOF LPAREN argumentos RPAREN
                | MUTABLESETOF LPAREN RPAREN
                | MUTABLESETOF LPAREN argumentos RPAREN
                | SETOF MENOR tipo MAYOR LPAREN RPAREN
                | MUTABLESETOF MENOR tipo MAYOR LPAREN RPAREN"""


# ------------------------------------------------------------------------------
# Lambdas: { a: Int, b: Int -> a + b }
# ------------------------------------------------------------------------------

# lambda con parámetros y cuerpo, se puede asignar con val f = { ... }
def p_lambda(p):
    "lambda_expr : LLAVEIZQ parametros_lambda ARROW sentencias LLAVEDER"


def p_parametros_lambda(p):
    """parametros_lambda : parametro_lambda
                         | parametros_lambda COMA parametro_lambda"""


# parámetro con tipo, tipo nullable, o sin tipo ({ x -> x * 2 })
def p_parametro_lambda(p):
    """parametro_lambda : ID COLON tipo
                        | ID COLON tipo_nullable
                        | ID"""
#---------------FIN DANIELA ESPINOZA--------------------------------------------

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