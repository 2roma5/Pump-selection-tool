import time
import numpy as np
import pandas as pd
from functions import Re, factor_friction, velocity, Hs
from functions import plot_data, friction, len_eq

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
}

len = {
    "vc": 8*(2.0670/39.37),
    "vg": 340*(2.0670/39.37),
    "vb": 150*(2.0670/39.37),
    "vm": 45*(2.0670/39.37),
    "vn": 100*(2.0670/39.37),
    "po": 10*(2.0670/39.37),
    "r": 10*(2.0670/39.37),
    "tp": 10*(2.0670/39.37),
    "cc": 30*(2.0670/39.37)
}

# Catálogo de accesorios (solo imprime las opciones)
def catalogo():
    print("Seleccione los accesorios presentes en su proceso: ")
    print("------------------------------------------------\n")
    print("\t     CATÁLOGO DE ACCESORIOS\n")
    print("1. Válvula de compuerta.  6. Placa de orificio.\n2. Válvula de globo.      7. Rotámetro.\n3. Válvula de bola.       8. Tubo pitot.\n4. Válvula de mariposa.   9. Codos\n5. Válvula check.         10. Salir.") 
    print("\n------------------------------------------------")


# Consigue las variables del proceso (accesorios)
def get_process(accesorios: dict[str, int]):
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
                accesorios["vn"] = accesorios["vn"] + c
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

# Consigue los requerimientos del proceso
def get_info(accesorios: dict[str, int]):
    print("¡Bienvenido, aquí podrás elegir la mejor bomba para tu proceso!")
    time.sleep(1.5)
    print("Por favor ingresa los requerimientos y características de tu proceso.")
    q = float(input("Ingresa el flujo que necesita tu proceso [L/min]: "))
    if q < 0:
        q = abs(q)
        print("¿Negativo?")
    catalogo()
    get_process(accesorios)
    idk()


def idk():
    z1 = float(input("Ingresa la elevación inicial: "))
    z2 = float(input("Ingresa la elevación final: "))
    l = float(input("Ingrese la longuitud de tubería recta: "))
    #z1 = float(z1)
    #z2 = float(z2)
    z1 = 120.5/100
    z2 = 316/100
    Q = np.linspace(0, 1000, 1000)
    Q_ = Q/1000/60
    densidad = 998.2
    viscosidad = 0.00105
    diametro = 2.0670/39.37
    longuitudT = len_eq(accesorios, len) + l
    velocidades = [velocity(q, diametro) for q in Q_]
    Reynolds = [Re(v, diametro, densidad, viscosidad) for v in velocidades]
    f_fricc = [factor_friction(diametro, 0.000046, r) for r in Reynolds]
    fricciones = [friction(f, diametro, v, longuitudT) for f, v in zip(
        f_fricc, velocidades)]
    cabeza = [Hs(0, 1, 998.2, v, v, z1, z2, f) for v, f in zip(
        velocidades, fricciones)]
    plot_data(Q, cabeza, "Cabeza vs Flujo", "Flujo [L/min]", "Cabeza [m]")
    df = pd.DataFrame({"Velocidad": velocidades, "Reynolds": Reynolds,
                       "Factor de fricciones": f_fricc, "Cabeza": cabeza,
                       "Fricciones": fricciones})
    print(df)
    input("Presiona Enter para continuar...")

