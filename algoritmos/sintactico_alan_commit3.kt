// Commit 3 - Alan Aguilar: Estructura de control when
var dia: Int = 3
var nombreDia: String = "Desconocido"

when (dia) {
    1 -> println("Lunes")
    2, 3 -> println("Martes o Miercoles")
    4, 5 -> {
        println("Jueves o Viernes")
        dia++
    }
    else -> println("Fin de semana")
}

var nota: Int = 8
var resultado: String = when (nota) {
    10 -> "Sobresaliente"
    8, 9 -> "Muy bueno"
    7 -> "Regular"
    else -> {
        println("Necesita recuperacion")
        "Insuficiente"
    }
}
