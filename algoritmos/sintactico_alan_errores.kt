// Errores de sintaxis a propósito para probar el analizador sintáctico de Alan

// Error 1: var sin tipo explícito (Alan requiere tipo obligatorio)
var edad = 20

// Error 2: operador inesperado en expresión aritmética
var total: Int = (precio * cantidad) + * 5

// Error 3: rama de when sin operador flecha (->)
when (codigo) {
    1 "Lunes"
    else -> "Otro"
}
