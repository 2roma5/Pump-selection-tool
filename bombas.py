import time
import numpy as np
from functions import Re, factor_friction, velocity, Hs
from functions import plot_data, friction, len_eq, bomba1, bomba1c, bomba3a
from functions import plot_2_data, find_intersections

# Accesorios
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

# Leq = (K*D)/f
len = {
    "vc": (0.15*0.052)/0.019,
    "vg": (6.5*0.052)/0.019,
    "vb": (0.1*0.052)/0.019,
    "vm": (0.7*0.052)/0.019,
    "vn": (2.75*0.052)/0.019,
    "po": (0.1*0.052)/0.019,
    "r": (7*0.052)/0.019,
    "tp": (7*0.052)/0.019,
    "cc": (0.7*0.052)/0.019
}


# Catálogo de accesorios (solo imprime las opciones)
def catalogo() -> None:
    print("\nSeleccione los accesorios presentes en su proceso: ")
    print("------------------------------------------------\n")
    print("\t     CATÁLOGO DE ACCESORIOS\n")
    print("1. Válvula de compuerta.  6. Placa de orificio.\n2. Válvula de globo.      7. Rotámetro.\n3. Válvula de bola.       8. Tubo pitot.\n4. Válvula de mariposa.   9. Codos\n5. Válvula check.         10. Salir.") 
    print("\n------------------------------------------------")


# Consigue las variables del proceso (accesorios)
def get_process(accesorios: dict[str, int]) -> None:
    while True:
        try:
            op = int(input("opción: "))
            if op == 1:
                c = int(input("¿Cuántas válvulas de compuerta tiene?: "))
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
def get_info() -> None:
    print("¡Bienvenido, aquí podrás elegir la mejor bomba para tu proceso!")
    time.sleep(1.5)
    print("Por favor ingresa los requerimientos y características de tu proceso.")
    global z1, z2, l, diametro, caudal
    caudal = float(input("Ingresa el flujo que necesita tu proceso [L/min]: "))
    if caudal < 0:
        caudal = abs(caudal)
        print("¿Negativo?")
    if caudal > 200:
        print("Lo sentimos, ninguna de nuestras bombas cumple este requerimiento.")
        get_info()
    z1 = float(input("Ingresa la elevación inicial [m]: "))
    if z1 < 0:
        z1 = abs(z1)
        print("¿Negativo?")
    z2 = float(input("Ingresa la elevación final [m]: "))
    if z2 < 0:
        z2 = abs(z2)
        print("¿Negativo?")
    l = float(input("Ingrese la longuitud de tubería recta [m]: "))
    if l < 0:
        l = abs(l)
        print("¿Negativo?")
    diametro = float(input("Ingrese el diámetro de su tubería [in]: "))
    if diametro < 0:
        diametro = abs(diametro)
        print("¿Negagivo?")
    diametro = diametro/39.37


# Calcula la cabeza del sistema y la presenta
def idk() -> None:
    Q = np.linspace(0, 180, 1000)
    Q_ = Q/180/60
    global densidad, viscosidad, longuitudT
    densidad = 998.2
    viscosidad = 0.00105
    longuitudT = len_eq(accesorios, len) + l
    velocidades = [velocity(q, diametro) for q in Q_]
    Reynolds = [Re(v, diametro, densidad, viscosidad) for v in velocidades]
    f_fricc = [factor_friction(diametro, 0.000046, r) for r in Reynolds]
    fricciones = [friction(f, diametro, v, longuitudT) for f, v in zip(
        f_fricc, velocidades)]
    cabeza = [Hs(0, 1, 998.2, v, v, z1, z2, f) for v, f in zip(
        velocidades, fricciones)]
    intersecciones1 = find_intersections(Q, bomba1(Q), cabeza)
    intersecciones2 = find_intersections(Q, bomba1c(Q), cabeza)
    intersecciones3 = find_intersections(Q, bomba3a(Q), cabeza)
    if head() < bomba1(caudal) and intersecciones1:
        print("La bomba con el tag B1 es ideal para tu proceso")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1c(caudal) and intersecciones2:
        print("La bomba con el tag B1C es ideal para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1c(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba3a(caudal) and intersecciones3:
        time.sleep(1)
        plot_data(Q, bomba3a(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1(caudal) and bomba1c(caudal) and intersecciones1 and intersecciones2:
        print("Las bombas con el tag B1 y B1C son ideales para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        plot_data(Q, bomba1c(Q), cabeza)
        plot_2_data(Q, bomba1(Q), bomba1c(Q), cabeza, "Bomba 1", "Bomba 1C")
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1(caudal) and bomba3a(caudal) and intersecciones1 and intersecciones3:
        print("Las bombas con el tag B1 y B3A son ideales para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        plot_data(Q, bomba3a(Q), cabeza)
        plot_2_data(Q, bomba1(Q), bomba3a(Q), cabeza, "Bomba 1", "Bomba 3A")
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1c(caudal) and bomba3a(caudal) and intersecciones2 and intersecciones3:
        print("Las bombas con el tag B1C y B3A son ideales para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1c(Q), cabeza)
        plot_data(Q, bomba3a(Q), cabeza)
        plot_2_data(Q, bomba1c(Q), bomba3a(Q), cabeza, "Bomba 1C", "Bomba 3A")
        print("¡Muchas gracias por usar nuestro programa!")
    else:
        print("Lo sentimos, ninguna de nuestras bombas es capaz de cumplir con tus requisitos.")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        plot_data(Q, bomba1c(Q), cabeza)
        plot_data(Q, bomba3a(Q), cabeza)


# Calcula el valor específico de la cabeza del sistema
def head() -> float:
    velocidad = velocity(caudal/180/60, diametro)
    reynolds = Re(velocidad, diametro, densidad, viscosidad)
    factor_de_friccion = (factor_friction(diametro, 0.000046, reynolds))
    fricciones = friction(factor_de_friccion, diametro, velocidad, longuitudT)
    return Hs(1, 1, 998.2, velocidad, velocidad, z1, z2, fricciones)


get_info()
catalogo()
get_process(accesorios)
idk()
