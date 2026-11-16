fun ok1(): Int { return 1 }
fun ok2(): String { return "hola" }
fun ok3(): Boolean { return true }
fun ok4() { while (true) { break } }
fun ok5() { while (true) { if (true) { continue } } }
fun ok6(): Int {
    val x = 10
    return x
}
fun mal1(): Int { return "a" }
fun mal2(): String { return 5 }
fun mal3(): Boolean {
    val n = 5
    return n
}
fun mal4() { break }
fun mal5() { continue }
fun mal6() { if (true) { break } }
fun mal7() { if (5) { println(1) } }
fun mal8() { while ("a") { break } }
fun mal10() {
    while (true) {
        break
    }
    break
}