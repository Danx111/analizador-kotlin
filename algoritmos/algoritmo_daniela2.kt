// ===== Constantes =====
const val MAX: Int = 10
const val SALUDO = "Hola"
const val PI_APROX: Double = 3.14

// ===== Variables nullables =====
var apodo: String? = null
val edad: Int? = 20
var correo: String?

// ===== Null-safety =====
val largo = apodo?.length
val largoSeguro = apodo?.length ?: 0
val nombre = apodo ?: "sin nombre"
val forzado = apodo!!
val largoForzado = apodo!!.length
val mayusculas = apodo?.uppercase()

apodo = "Dani"
println(apodo ?: "vacio")

// ===== Booleanas, comparación y rango =====
val a = 5 > 3 && 2 < 4
val b = 1 == 1 || 2 != 2
val c = !true
val d = 10 >= 5 && 3 <= 3
val rango = 1..10
val rangoVar = 1..MAX

// ===== Conjuntos =====
val numeros = setOf(1, 2, 3, 3)
val letras = mutableSetOf("a", "b")
val vacio = setOf<Int>()
val vacioMut = mutableSetOf<String>()
val tipado: Set<Int> = setOf(1, 2)
val tipadoMut: MutableSet<String> = mutableSetOf("x")
letras.add("c")
println(numeros.size)

// ===== while =====
var i: Int? = 0
while (i < 5) {
    println(i)
    i += 1
}

while (true) {
    break
}

// ===== for sobre rango =====
for (k in 1..10) {
    println(k)
}

// ===== for sobre colección =====
for (item in numeros) {
    println(item)
}

for (letra in letras) {
    if (letra == "b") {
        continue
    }
    println(letra)
}

// ===== for y while anidados =====
for (x in 1..3) {
    var j: Int? = 0
    while (j < x) {
        println(j)
        j += 1
    }
}

// ===== Lambdas =====
val mayor = { a: Int, b: Int -> a > b }
val esPar = { n: Int -> n == 0 }
val sinTipo = { x -> x }
val nullable = { s: String? -> s ?: "vacio" }
val saludar = { nombre: String -> println(nombre) }

println(mayor(3, 2))
println(saludar("Daniela"))