import time
import numpy as np
from functions import Re, factor_friction, velocity, Hs, head
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

# Parámetros de fluido y proceso
param = {
    "len": 0.0,
    "densi": 998.2,
    "lent": 0.0,
    "mu": 0.00105,
    "dia": 0.0,
    "Q": 0.0,
    "z1": 0.0,
    "z2": 0.0
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
def get_process(accesorios: dict[str, int]) -> bool:
        try:
            op = int(input("opción: "))
            if op == 1:
                c = int(input("¿Cuántas válvulas de compuerta tiene?: "))
                accesorios["vc"] += c
                return True
            elif op == 2:
                c = int(input("¿Cuántas válvulas de globo tiene?: "))
                accesorios["vg"] += c
                return True
            elif op == 3:
                c = int(input("¿Cuántas válvulas de bola tiene?: "))
                accesorios["vb"] += c
                return True
            elif op == 4:
                c = int(input("¿Cuántas válvulas de mariposa tiene?: "))
                accesorios["vm"] += c
                return True
            elif op == 5:
                c = int(input("Cuántas válvulas check tiene?: "))
                accesorios["vn"] += c
                return True
            elif op == 6:
                c = int(input("¿Cuántas placas de orificio tiene?: "))
                accesorios["po"] += c
                return True
            elif op == 7:
                c = int(input("¿Cuántos rotámetros tiene?: "))
                accesorios["r"] += c
                return True
            elif op == 8:
                c = int(input("¿Cuántos tubos de pitot tiene?: "))
                accesorios["tp"] += c
                return True
            elif op == 9:
                c = int(input("¿Cuántos codos tiene?: "))
                accesorios["cc"] += c
                return True
            elif op == 10:
                print("¡Gracias!\n")
                return False
            else:
                print("Esa no es una opción, intente de nuevo.")
        except ValueError:
            print("Solo se admiten números, inténtelo de nuevo.")

# Consigue los requerimientos del proceso
def get_info() -> None:
    print("¡Bienvenido, aquí podrás elegir la mejor bomba para tu proceso!")
    print("Por favor ingresa los requerimientos y características de tu proceso.")
    param["Q"] += float(input("Ingresa el flujo que necesita tu proceso [L/min]: "))
    if param["Q"] < 0:
        param["Q"] = abs(param["Q"])
        print("¿Negativo?")
    if param["Q"] > 200:
        print("Lo sentimos, ninguna de nuestras bombas cumple este requerimiento.")
        get_info()
    param["z1"] += float(input("Ingresa la elevación inicial [m]: "))
    if param["z1"] < 0:
        param["z1"] = abs(param["z1"])
        print("¿Negativo?")
    param["z2"] = float(input("Ingresa la elevación final [m]: "))
    if param["z2"] < 0:
        param["z2"] = abs(param["z2"])
        print("¿Negativo?")
    param["len"] = float(input("Ingrese la longuitud de tubería recta [m]: "))
    if param["len"] < 0:
        param["len"] = abs(param["len"])
        print("¿Negativo?")
    param["dia"] = float(input("Ingrese el diámetro de su tubería [in]: "))
    if param["dia"] < 0:
        param["dia"] = abs(param["dia"])
        print("¿Negagivo?")
    param["dia"] /= 39.37
    catalogo()
    while get_process(accesorios) == True:
        if get_process(accesorios) == False:
            break
    idk()

# Calcula la cabeza del sistema y la presenta
def idk() -> None:
    Q = np.linspace(0, 180, 1000)
    Q_ = Q/180/60
    param["lent"] = len_eq(accesorios, len) + param["len"]
    velocidades = [velocity(q, param["dia"]) for q in Q_]
    Reynolds = [Re(v, param["dia"], param["densi"], param["mu"]) for v in velocidades]
    f_fricc = [factor_friction(param["dia"], 0.000046, r) for r in Reynolds]
    fricciones = [friction(f, param["dia"], v, param["lent"]) for f, v in zip(
        f_fricc, velocidades)]
    cabeza = [Hs(1, 1, 998.2, v, v, param["z1"], param["z2"], f) for v, f in zip(
        velocidades, fricciones)]
    intersecciones1 = find_intersections(Q, bomba1(Q), cabeza)
    intersecciones2 = find_intersections(Q, bomba1c(Q), cabeza)
    intersecciones3 = find_intersections(Q, bomba3a(Q), cabeza)
    hs = head(param["Q"], param["dia"], param["densi"], param["mu"], param["lent"], param["z1"], param["z2"])
    if hs < bomba1(param["Q"]) and intersecciones1:
        print("La bomba con el tag B1 es ideal para tu proceso")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif hs < bomba1c(param["Q"]) and intersecciones2:
        print("La bomba con el tag B1C es ideal para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1c(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif hs < bomba3a(param["Q"]) and intersecciones3:
        time.sleep(1)
        plot_data(Q, bomba3a(Q), cabeza)
        print("¡Muchas gracias por usar nuestro programa!")
    elif hs < bomba1(param["Q"]) and bomba1c(param["Q"]) and intersecciones1 and intersecciones2:
        print("Las bombas con el tag B1 y B1C son ideales para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        plot_data(Q, bomba1c(Q), cabeza)
        plot_2_data(Q, bomba1(Q), bomba1c(Q), cabeza, "Bomba 1", "Bomba 1C")
        print("¡Muchas gracias por usar nuestro programa!")
    elif hs < bomba1(param["Q"]) and bomba3a(param["Q"]) and intersecciones1 and intersecciones3:
        print("Las bombas con el tag B1 y B3A son ideales para tu proceso.")
        time.sleep(1)
        plot_data(Q, bomba1(Q), cabeza)
        plot_data(Q, bomba3a(Q), cabeza)
        plot_2_data(Q, bomba1(Q), bomba3a(Q), cabeza, "Bomba 1", "Bomba 3A")
        print("¡Muchas gracias por usar nuestro programa!")
    elif hs < bomba1c(param["Q"]) and bomba3a(param["Q"]) and intersecciones2 and intersecciones3:
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
    print(hs)
    print(bomba1(param["Q"]))

def main():
    get_info()

if __name__ == '__main__':
    main()

