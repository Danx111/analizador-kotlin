// Commit 4 - Alan Aguilar: Algoritmo válido para probar el analizador semántico

// 1. Declaraciones con tipo explícito, nullables y colecciones Map
var edad: Int = 20
var saldo: Double = 150.5
var usuario: String = "Alan"
var apodo: String? = null
var activo: Boolean = true
var inicial: Char = 'A'
var precios: Map<String, Double> = mutableMapOf("pan" to 1.5, "cafe" to 2.0)

// 2. Funciones de expresión única con parámetros por defecto compatibles
fun saludar(nombre: String = "invitado"): String = "Hola, " + nombre
fun calcularBono(base: Int, extra: Int = 10): Int = base + extra * 2

// 3. Operaciones aritméticas, unarios, compuestas y concatenación válida
var total: Int = (edad + 5) * 2 - 4 / 2 % 3
var negativo: Int = -edad
total++
total--
total += 15
total -= 5

var mensaje: String = "Edad: " + edad
mensaje += " anios"

// 4. Reasignaciones válidas (incluyendo null en variable nullable)
apodo = "Alancito"
apodo = null
edad = calcularBono(edad)

// 5. Estructura when con expresiones válidas
var categoria: String = when (total) {
    10 -> "Bajo"
    20, 30 -> "Medio"
    else -> "Alto"
}
println(saludar(usuario))
println(mensaje)
