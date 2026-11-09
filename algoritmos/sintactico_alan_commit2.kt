// Commit 2 - Alan Aguilar: Declaración var con tipo explícito y Map / MutableMap
var edad: Int = 20
var tasa: Double = 0.15
var mensaje: String = "Kotlin"

var capitales: Map<String, String> = mapOf("Ecuador" to "Quito", "Colombia" to "Bogota")
var inventario: MutableMap<String, Int> = mutableMapOf("cuadernos" to 100, "lapices" to 250)
var catalogo: Map<String, Double> = mutableMapOf<String, Double>()

inventario["cuadernos"] = 120
var totalArticulos: Int = inventario["cuadernos"] + inventario["lapices"]
