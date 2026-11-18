// Registro de notas con un error de cada tipo para el informe final
// Mateo Andrade

const val NOTA_MINIMA = 7

fun promedio(notas: List<Int>): Double {
    var suma: Int = 0
    for (nota in notas) {
        suma += nota
    }
    return suma.toDouble() / notas.size
}

fun main() {
    val notas = listOf(8, 6, 9, 10)
    val final = promedio(notas)
    var aprobados: Int = 0 #

    for (nota in notas) {
        if (nota >= NOTA_MINIMA) {
            aprobados++
        }
    }

    if (final > 5 {
        println("Curso aprobado")
    }

    NOTA_MINIMA = 5
    println("Aprobados: " + aprobados)
    println(reprobados)
}
