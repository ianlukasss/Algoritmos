def romano_a_decimal(romano):
    valores = {
        'I': 1, 'V': 5, 'X': 10,
        'L': 50, 'C': 100,
        'D': 500, 'M': 1000
    }

    total = 0
    previo = 0

    for letra in romano:
        if letra not in valores:
            return "Error: número romano inválido"

        valor = valores[letra]

        if valor > previo:
            total += valor - 2 * previo
        else:
            total += valor

        previo = valor

    return total

while True:
    romano = input("Ingrese un número romano: ").upper()

    resultado = romano_a_decimal(romano)
    print("Resultado:", resultado)

    continuar = input("¿Querés ingresar otro número? (si/no): ").lower()

    if continuar != 'si':
        print("Programa finalizado.")
        break