// Commit 4 - Alan Aguilar: Funciones de expresión única y parámetros con valor por defecto
// Integración completa de las características sintácticas 

// 1. Funciones de expresión única con parámetro por defecto
fun saludar(nombre: String = "invitado"): String = "Hola"
fun duplicar(numero: Int = 1): Int = numero * 2
fun calcularTarifa(base: Double, factor: Double = 1.25): Double = base * factor + 5.0

// 2. Declaración var con tipo explícito y estructuras Map / MutableMap
var usuario: String = "Alan"
var saludo: String = saludar(usuario)
var precios: MutableMap<String, Double> = mutableMapOf("pan" to 1.5, "cafe" to 2.0)
var catalogo: Map<String, String> = mapOf("A" to "Alfa", "B" to "Beta")

// 3. Modificación y reasignación con expresiones aritméticas
precios["pan"] = precios["pan"] + 0.5
var contador: Int = duplicar(5)
contador++

// 4. Estructura de control when
var codigo: Int = 2
var categoria: String = when (codigo) {
    1 -> "Administrador"
    2, 3 -> "Editor"
    4, 5 -> {
        println("Acceso basico")
        "Lector"
    }
    else -> "Invitado"
}
