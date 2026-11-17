// 1. Constantes (con tipo explícito e inferido)
const val LIMITE_INTENTOS: Int = 5
const val APP_NOMBRE = "SistemaNotas"

fun main() {
    // 2. Declaración de variables con tipos básicos y nullables
    var apodo: String? = null
    var usuario: String?
    val activo: Boolean = true
    var contador: Int = 0

    // 3. Conjuntos (Set y MutableSet) acotados a Int y String
    val idsPermitidos: Set<Int> = setOf(101, 102, 103)
    var etiquetas: MutableSet<String> = mutableSetOf("kotlin", "compiladores")
    val vacioEnteros = setOf<Int>()
    var vacioTextos = mutableSetOf<String>() 

    // 4. Operadores de Null-Safety (Elvis ?:, Safe Call ?., Not-Null Assert !!)
    val nombreMostrar: String = apodo ?: "Invitado"
    val longitudApodo = apodo?.length
    val apodoMayus = apodo?.uppercase()

    apodo = "Daniela"
    val largoSeguro = apodo!!.length
    val textoForzado = apodo!!

    // 5. Operadores lógicos (&&, ||, !) y relacionales (==, !=, <, >, <=, >=)
    val puedeEntrar: Boolean = activo && (contador < LIMITE_INTENTOS) || !false
    val sonDiferentes: Boolean = (contador != 10) && (LIMITE_INTENTOS >= 5)

    // 6. Ciclo WHILE con break y continue
    while (contador < LIMITE_INTENTOS && activo) {
        contador = contador + 1
        if (contador == 2) {
            continue
        }
        if (contador > 4) {
            break
        }
    }

    // 7. Ciclo FOR sobre rango (1..10) y sobre colección (Set)
    for (i in 1..5) {
        println(i)
    }

    for (id in idsPermitidos) {
        if (id <= 102) {
            println(id)
        }
    }

    // 8. Expresiones Lambda (con tipo explícito, nullable y sin tipo)
    val sumar = { a: Int, b: Int -> a + b }
    val duplicar = { x -> x * 2 }
    val saludar = { nombre: String? -> println(nombre) }
}