// Registro de notas de un curso
// Lee las notas por teclado, calcula el promedio y clasifica a cada estudiante

/* Algoritmo de prueba
   Mateo Andrade */

fun sumar(a: Int, b: Int): Int {
    return a + b
}

fun promedio(notas: List<Int>): Double {
    var suma: Int = 0
    for (nota in notas) {
        suma = sumar(suma, nota)
    }
    return suma.toDouble() / notas.size
}

fun clasificar(nota: Double): String {
    if (nota >= 9.0) {
        return "Excelente"
    } else if (nota >= 7.0) {
        return "Aprobado"
    } else if (nota >= 5.0) {
        return "Recuperacion"
    } else {
        return "Reprobado"
    }
}

fun mostrarLista(titulo: String, valores: List<Int>) {
    println(titulo)
    for (valor in valores) {
        print(valor)
        print(" ")
    }
    println()
}

fun main() {
    val curso = "Lenguajes de Programacion"
    val paralelo = 1
    val notaMaxima = 10.0
    val bono = 0.5f
    val poblacion = 1_000_000L
    println("Curso: " + curso)

    val estudiantes = mutableListOf("Ana", "Luis", "Sofia")
    val notasAna = listOf(8, 9, 10)
    val notasLuis = listOf(6, 5, 7)
    val notasSofia = mutableListOf<Int>()

    println("Ingrese la primera nota de Sofia:")
    val primera = readln().toInt()
    notasSofia.add(primera)
    println("Ingrese la segunda nota de Sofia:")
    val segunda = readLine()
    notasSofia.add(9)
    notasSofia[0] = primera + 1

    estudiantes.add("Pedro")
    val cantidad = estudiantes.size

    val promedioAna = promedio(notasAna)
    val promedioLuis = promedio(notasLuis)
    val promedioSofia = promedio(notasSofia)

    println(clasificar(promedioAna))
    println(clasificar(promedioLuis))
    println(clasificar(promedioSofia))

    val mejor = if (promedioAna > promedioLuis) "Ana" else "Luis"
    val letra = if (promedioAna >= 9.0) 'A' else if (promedioAna >= 7.0) 'B' else 'C'

    if (cantidad > 3 && promedioAna > 7.0) {
        println("Curso completo y Ana aprobada")
    }

    mostrarLista("Notas de Ana:", notasAna)
    println(mejor)
    println(letra)
}
