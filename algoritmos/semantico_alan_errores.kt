// Commit 4 - Alan Aguilar: Algoritmo con errores semánticos intencionales ([Tipos] y [Operación])

// === Regla 1: Compatibilidad de tipos y nullabilidad ([Tipos]) ===
var edad: Int = "veinte"
val s: String = null
var apodo: String? = "Ana"
var nombre: String = apodo

var contador: Int = 10
contador = "diez"
contador = null

const val LIMITE: Int = "cien"
fun duplicar(x: Int = "mal"): Int = x * 2

// === Regla 2: Operaciones permitidas ([Operación]) ===
val restaTexto = "hola" - 2
val multBool = true * 3
val divChar = 'a' / 2
val sumaDerecha = 20 + " anios"
val sumaBool = true + 1

var texto: String = "Kotlin"
val negTexto = -texto
texto++
texto -= "K"
contador += "5"
