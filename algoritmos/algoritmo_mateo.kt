// Promedio de notas

/* Algoritmo de prueba
   Mateo Andrade */
const val NOTA_MINIMA = 7

fun promedio(notas: List<Int>): Double {
    var suma = 0.0
    for (nota in notas) {
        suma += nota
    }
    return suma / notas.size
}

fun main() {
    val notas = listOf(8, 6, 10)
    var pendientes = mutableListOf(5, 9)

    val poblacion = 1_000_000
    val grande = 10L
    val pi = 3.14
    val precio = 2.5f
    val dos = 2f

    var total = (poblacion + grande) * 2 - pendientes.size / 4 % 3
    total += 1
    total -= 2
    total *= 3
    total /= 4
    total %= 5

    for (i in 1..10) {
        total = total + i
    }

    val resultado = promedio(notas)
    if (resultado >= NOTA_MINIMA) {
        println("Aprobado")
    } else {
        println("Reprobado")
    }

    val error = # @
    /* comentario sin cerrar
}
