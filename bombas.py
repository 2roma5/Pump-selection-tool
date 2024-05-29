import time
import numpy as np
from functions import Re, factor_friction

# Variables del proceso
accesorios = {
    "vc": 0,
    "vg": 0,
    "vb": 0,
    "vm": 0,
    "vn": 0,
    "po": 0,
    "r": 0,
    "tp": 0,
    "cc": 0,
    "rn": 0,
    "rho": 0,
    "mu": 0
}


# Catálogo de accesorios (solo imprime las opciones)
def catalogo():
    print("Seleccione los accesorios presentes en su proceso: ")
    print("------------------------------------------------\n")
    print("\t     CATÁLOGO DE ACCESORIOS\n")
    print("1. Válvula de compuerta.  6. Placa de orificio.\n2. Válvula de globo.      7. Rotámetro.\n3. Válvula de bola.       8. Tubo pitot.\n4. Válvula de mariposa.   9. Codos\n5. Válvula check.         10. Salir.") 
    print("\n------------------------------------------------")


# Consigue las variables del proceso (accesorios)
def get_process(accesorios: dict):
    while True:
        try:
            op = int(input("opción: "))
            if op == 1:
                c = int(input("¿Cuántas válvulas de compuesta tiene?: "))
                accesorios["vc"] = accesorios["vc"] + c
                get_process(accesorios)
            elif op == 2:
                c = int(input("¿Cuántas válvulas de globo tiene?: "))
                accesorios["vg"] = accesorios["vg"] + c
                get_process(accesorios)
            elif op == 3:
                c = int(input("¿Cuántas válvulas de bola tiene?: "))
                accesorios["vb"] = accesorios["vb"] + c
                get_process(accesorios)
            elif op == 4:
                c = int(input("¿Cuántas válvulas de mariposa tiene?: "))
                accesorios["vm"] = accesorios["vm"] + c
                get_process(accesorios)
            elif op == 5:
                c = int(input("Cuántas válvulas check tiene?: "))
                accesorios["vc"] = accesorios["vc"] + c
                get_process(accesorios)
            elif op == 6:
                c = int(input("¿Cuántas placas de orificio tiene?: "))
                accesorios["po"] = accesorios["po"] + c
                get_process(accesorios)
            elif op == 7:
                c = int(input("¿Cuántos rotámetros tiene?: "))
                accesorios["r"] = accesorios["r"] + c
                get_process(accesorios)
            elif op == 8:
                c = int(input("¿Cuántos tubos de pitot tiene?: "))
                accesorios["tp"] = accesorios["tp"] + c
                get_process(accesorios)
            elif op == 9:
                c = int(input("¿Cuántos codos tiene?: "))
                accesorios["cc"] = accesorios["cc"] + c
                get_process(accesorios)
            elif op == 10:
                print("¡Gracias!\n")
                break
            else:
                print("Esa no es una opción, intente de nuevo.")
                get_process(accesorios)
            break
        except ValueError:
            print("Solo se admiten números, inténtelo de nuevo.")


# Consigue descripción del fluido
def get_fluid(accesorios: dict):
    c = float(input("Ahora, ingresa el radio nominal de tus tuberías: "))
    accesorios["rn"] = accesorios["rn"] + c
    if accesorios["rn"] < 0:
        accesorios["rn"] = abs(accesorios["rn"])
        print("¿?")
    print("Ahora, hablamos acerca de que estás transportando.")
    c = float(input("Ingresa la densidad de tu fluido: "))
    accesorios["rho"] = accesorios["rho"] + c
    if accesorios["rho"] < 0:
        accesorios["rho"] = abs(accesorios["rho"])
        print("Error fatal, basta por favor.")
    c = float(input("Ingresa la viscocidad de tu fluido: "))
    accesorios["mu"] = accesorios["mu"] + c
    if accesorios["mu"] < 0:
        accesorios["mu"] = abs(accesorios["mu"])
        print("Error fatal, deja de jugar con nosotros, sabemos dónde vives.")


# Consigue los requerimientos del proceso
def get_info(accesorios: dict):
    print("¡Bienvenido, aquí podrás elegir la mejor bomba para tu proceso!")
    time.sleep(1.5)
    print("Por favor ingresa los requerimientos y características de tu proceso.")
    h = float(input("Ingresa la cabeza que necesita tu proceso [m]: "))
    if h < 0:
        h = abs(h)
        print("¿Negativo?")
    q = float(input("Ingresa el flujo que necesita tu proceso [L/min]: "))
    if q < 0:
        q = abs(q)
        print("¿Negativo?")
    catalogo()
    get_process(accesorios)
    get_fluid(accesorios)
    idk()


def idk():
    z1 = input("Ingresa la elevación inicial: ")
    z2 = input("Ingresa la elevación final: ")
    dz = float(z2) - float(z1)
    Q = np.linspace(0, 1000, 1000)
    area = 20
    velocidades = [q/area for q in Q]
    densidad = 1000
    viscosidad = 0.001
    diametro = 0.1
    Reynolds = [Re(v, diametro, densidad, viscosidad) for v in velocidades]
    fricciones = [factor_friction(diametro, 0.0001, r) for r in Reynolds]
    print(dz)
    print(fricciones)

def main(): -> None
    get_info(accesorios)
    print(accesorios)

if __name__ == '__main__'
    main()
