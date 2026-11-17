# KotlinScope: analizador de Kotlin

Analizador léxico, sintáctico y semántico para un subconjunto de Kotlin, hecho en Python con PLY y una interfaz gráfica en Tkinter.

Proyecto de Lenguajes de Programación (CCPG1048), ESPOL, PAO II 2026.

| Integrante | GitHub |
|---|---|
| Andrade Domínguez Mateo Andrés | `mateoandraded` |
| Aguilar Morocho Alan Ariel | `alan-am` |
| Espinoza Toala Daniela Joselyne | `Danx111` |

## Qué hay que instalar

| Requisito | Versión | Cómo se instala |
|---|---|---|
| Python | 3.10 o superior (probado con 3.12 y 3.13) | https://www.python.org/downloads/ |
| PLY | 3.11 | `pip install -r requirements.txt` |
| Tkinter | viene con Python | En Windows y macOS ya está incluido. En Linux: `sudo apt install python3-tk` |

No se usa ninguna otra librería.

```bash
pip install -r requirements.txt
```

## Cómo se usa

Todos los comandos se corren desde la carpeta raíz del proyecto (donde está este README).

### Interfaz gráfica

```bash
python main.py
```

1. Escribe código Kotlin en el editor, abre un `.kt` con **Abrir .kt** o elige uno de la lista **Algoritmo**.
2. Elige tu usuario de GitHub. El log se guarda con ese nombre.
3. Presiona **Léxico** (azul), **Sintáctico** (naranja) o **Semántico** (morado).
4. Los errores salen en la pestaña **Errores** con su fase y número de línea, y esas líneas se marcan en el editor. Al hacer clic en un error se resalta su línea y se muestra el mensaje completo.
5. La pestaña **Tokens** muestra cada token con su línea, tipo y valor. La pestaña **Log** muestra el log que se acaba de guardar.
6. La barra de abajo dice si el código es válido o cuántos errores tiene, y dónde quedó el log.

### Línea de comandos

```bash
python -m src.lexer algoritmos/algoritmo_mateo.kt mateoandraded
python -m src.parser algoritmos/algoritmo_mateo.kt mateoandraded
```

`src.lexer` genera el log léxico. `src.parser` genera los logs sintáctico y semántico.

## Logs

Cada análisis guarda un archivo en `logs/` con el formato `tipo-usuarioGit-ddmmaaaa-HHhMM.txt`, por ejemplo `semantico-mateoandraded-15112026-19h25.txt`.

## Estructura

```
main.py              abre la interfaz gráfica
src/lexer.py         analizador léxico (ply.lex)
src/parser.py        analizador sintáctico (ply.yacc) y reglas semánticas
src/gui.py           interfaz gráfica (Tkinter)
algoritmos/          algoritmos de prueba de cada integrante
logs/                logs de cada análisis
requirements.txt     dependencias
```

## Algoritmos de prueba

| Integrante | Programa válido | Programas con errores |
|---|---|---|
| Mateo Andrade | `algoritmo_mateo.kt` | `algoritmo_mateo_errores.kt` (sintácticos), `semantico_mateo_errores.kt` (semánticos) |
| Alan Aguilar | `semantico_alan.kt`, `sintactico_alan_commit2.kt` a `commit4.kt` | `sintactico_alan_errores.kt`, `semantico_alan_errores.kt` |
| Daniela Espinoza | `algoritmo_daniela2.kt` | `algoritmo_daniela.kt` (léxicos), `algoritmo_daniela_errores.kt`, `algoritmo_daniela_semantico.kt` |

## Reglas semánticas

| Integrante | Regla 1 | Regla 2 |
|---|---|---|
| Mateo Andrade | **Identificadores**: una variable o función debe estar declarada antes de usarse | **Asignación**: un `val`, `const val`, parámetro o variable del `for` no se puede reasignar |
| Alan Aguilar | **Tipos**: el valor debe ser compatible con el tipo declarado, incluido `null` solo en tipos `?` | **Operación**: los operadores solo se aplican a tipos permitidos |
| Daniela Espinoza | **Retorno**: una función debe retornar el tipo que declara | **Control**: `break`/`continue` solo dentro de un bucle y condiciones de tipo `Boolean` |

## Errores que reporta

- **Léxicos**: carácter no reconocido y comentario sin cerrar.
- **Sintácticos** (los dos casos de `p_error` de PLY): token inesperado, con su valor, tipo y línea, y fin de archivo inesperado, cuando falta cerrar una llave o un paréntesis. Después de un error el parser se recupera y sigue buscando más.
- **Semánticos**: `Error semántico [Categoría]: mensaje en la línea N`.
