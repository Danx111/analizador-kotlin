// Errores semánticos a propósito para probar mis dos reglas

const val NOTA_MAXIMA = 10

fun promedio(notas: List<Int>): Double {
    var suma: Int = 0
    for (nota in notas) {
        suma += nota
        nota = 0
    }
    notas = listOf(1, 2)
    return suma.toDouble() / notas.size
}

fun main() {
    val curso = "Lenguajes"
    var intentos: Int = 3
    intentos = intentos - 1

    curso = "Otro curso"
    NOTA_MAXIMA = 20

    println(total)
    val final = promedio(listOf(8, 9)) + bono
    imprimirReporte(final)

    println(aprobados)
    val aprobados = 5
    println(aprobados)
}
