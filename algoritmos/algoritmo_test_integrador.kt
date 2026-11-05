// Calcula el promedio de notas de un estudiante y lo clasifica
val notas = mapOf("Lengua" to 8.5, "Matematicas" to 6.0, "Ciencias" to 9.0)
var suma = 0.0
var contador = 0

/* Recorre las materias del mapa
   y acumula las notas */
for (materia in notas.keys) {
    suma += notas[materia]!!
    contador++
}

val promedio = suma / contador
val letra: Char = if (promedio >= 9.0) 'A' else if (promedio >= 7.0) 'B' else 'C'

when (letra) {
    'A' -> println("Excelente")
    'B' -> println("Aprobado")
    else -> println("Reprobado")
}

var intentos = 3
while (intentos > 0 && promedio < 7.0) {
    println("Debe rendir recuperacion")
    intentos--
}
