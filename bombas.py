import time
import numpy as np
from functions import Re, factor_friction, velocity, Hs
from functions import plot_data, friction, len_eq, bomba1, bomba1c, bomba3a
from functions import plot_2_data, find_intersections, catalogo

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


parametros = {
    "len": 0,
    "densi": 998.2,
    "lent": 0,
    "mu": 0.00105,
    "dia": 0,
    "Q": 0,
    "z1": 0,
    "z2": 0
}

#Diámetro promedio de tuberías [m]
D = 0.052 

#Factor de fricción promedio para acero
f = 0.019

# Leq = (K*D)/f
len = {
    "vc": (0.15*D)/f, 
    "vg": (6.5*D)/f, 
    "vb": (0.1*D)/f, 
    "vm": (0.7*D)/f, 
    "vn": (2.75*D)/f,
    "po": (0.1*D)/f,
    "r": (7*D)/f,
    "tp": (7*D)/f,
    "cc": (0.7*D)/f
}

# Consigue las variables del proceso (accesorios)
def get_process(accesorios: dict[str, int]) -> None:
    while True:
        try:
            op = int(input("opción: "))
            if op == 1:
                c = int(input("¿Cuántas válvulas de compuerta tiene?: "))
                accesorios["vc"] += c
                get_process(accesorios)
            elif op == 2:
                c = int(input("¿Cuántas válvulas de globo tiene?: "))
                accesorios["vg"] += c
                get_process(accesorios)
            elif op == 3:
                c = int(input("¿Cuántas válvulas de bola tiene?: "))
                accesorios["vb"] += c
                get_process(accesorios)
            elif op == 4:
                c = int(input("¿Cuántas válvulas de mariposa tiene?: "))
                accesorios["vm"] += c
                get_process(accesorios)
            elif op == 5:
                c = int(input("Cuántas válvulas check tiene?: "))
                accesorios["vn"] += c
                get_process(accesorios)
            elif op == 6:
                c = int(input("¿Cuántas placas de orificio tiene?: "))
                accesorios["po"] += c
                get_process(accesorios)
            elif op == 7:
                c = int(input("¿Cuántos rotámetros tiene?: "))
                accesorios["r"] += c
                get_process(accesorios)
            elif op == 8:
                c = int(input("¿Cuántos tubos de pitot tiene?: "))
                accesorios["tp"] += c
                get_process(accesorios)
            elif op == 9:
                c = int(input("¿Cuántos codos tiene?: "))
                accesorios["cc"] += c
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
    print("Por favor ingresa los requerimientos y características de tu proceso.")
    parametros["Q"] += float(input("Ingresa el flujo que necesita tu proceso [L/min]: "))
    if parametros["Q"] < 0:
        parametros["Q"] = abs(parametros["Q"])
        print("¿Negativo?")
    if parametros["Q"] > 200:
        print("Lo sentimos, ninguna de nuestras bombas cumple este requerimiento.")
        get_info()
    parametros["z1"] += float(input("Ingresa la elevación inicial [m]: "))
    if parametros["z1"] < 0:
        parametros["z1"] = abs(parametros["z1"])
        print("¿Negativo?")
    parametros["z2"] = float(input("Ingresa la elevación final [m]: "))
    if parametros["z2"] < 0:
        parametros["z2"] = abs(parametros["z2"])
        print("¿Negativo?")
    parametros["len"] = float(input("Ingrese la longuitud de tubería recta [m]: "))
    if parametros["len"] < 0:
        parametros["len"] = abs(parametros["len"])
        print("¿Negativo?")
    parametros["dia"] = float(input("Ingrese el diámetro de su tubería [in]: "))
    if parametros["dia"] < 0:
        parametros["dia"] = abs(parametros["dia"])
        print("¿Negagivo?")
    parametros["dia"] /= 39.37

# Calcula la cabeza del sistema y la presenta
def idk() -> None:
    Q = np.linspace(0, 180, 1000)
    Q_ = Q/180/60
    parametros["lent"] = len_eq(accesorios, len) + parametros["len"]
    velocidades = [velocity(q, parametros["dia"]) for q in Q_]
    Reynolds = [Re(v, parametros["dia"], parametros["densi"], parametros["mu"]) for v in velocidades]
    f_fricc = [factor_friction(parametros["dia"], 0.000046, r) for r in Reynolds]
    fricciones = [friction(f, parametros["dia"], v, parametros["lent"]) for f, v in zip(
        f_fricc, velocidades)]
    cabeza = [Hs(0, 1, 998.2, v, v, parametros["z1"], parametros["z2"], f) for v, f in zip(
        velocidades, fricciones)]
    intersecciones1 = find_intersections(Q, bomba1(Q), cabeza)
    intersecciones2 = find_intersections(Q, bomba1c(Q), cabeza)
    intersecciones3 = find_intersections(Q, bomba3a(Q), cabeza)
    if head() < bomba1(parametros["Q"]) and intersecciones1:
        print("La bomba con el tag B1 es ideal para tu proceso")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1c(parametros["Q"]) and intersecciones2:
        print("La bomba con el tag B1C es ideal para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1c(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba3a(parametros["Q"]) and intersecciones3:
        time.sleep(1)
        plot_data(Q, bomba3a(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1(parametros["Q"]) and bomba1c(parametros["Q"]) and intersecciones1 and intersecciones2:
        print("Las bombas con el tag B1 y B1C son ideales para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        plot_data(Q, bomba1c(Q), cabeza)
        plot_2_data(Q, bomba1(Q), bomba1c(Q), cabeza, "Bomba 1", "Bomba 1C")
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1(parametros["Q"]) and bomba3a(parametros["Q"]) and intersecciones1 and intersecciones3:
        print("Las bombas con el tag B1 y B3A son ideales para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        plot_data(Q, bomba3a(Q), cabeza)
        plot_2_data(Q, bomba1(Q), bomba3a(Q), cabeza, "Bomba 1", "Bomba 3A")
        print("¡Muchas gracias por usar nuestro programa!")
    elif head() < bomba1c(parametros["Q"]) and bomba3a(parametros["Q"]) and intersecciones2 and intersecciones3:
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
    velocidad = velocity(parametros["Q"]/180/60, parametros["dia"])
    reynolds = Re(velocidad, parametros["dia"], parametros["densi"], parametros["mu"])
    factor_de_friccion = (factor_friction(parametros["dia"], 0.000046, reynolds))
    fricciones = friction(factor_de_friccion, parametros["dia"], velocidad, parametros["lent"])
    return Hs(1, 1, 998.2, velocidad, velocidad, parametros["z1"], parametros["z2"], fricciones)


get_info()
catalogo()
get_process(accesorios)
idk()
