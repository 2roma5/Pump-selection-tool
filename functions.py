import matplotlib.pyplot as plt
from math import log10

# Catálogo de accesorios (solo imprime las opciones)
def catalogo() -> None:
    print("\nSeleccione los accesorios presentes en su proceso: ")
    print("------------------------------------------------\n")
    print("\t     CATÁLOGO DE ACCESORIOS\n")
    print("1. Válvula de compuerta.  6. Placa de orificio.\n2. Válvula de globo.      7. Rotámetro.\n3. Válvula de bola.       8. Tubo pitot.\n4. Válvula de mariposa.   9. Codos\n5. Válvula check.         10. Salir.") 
    print("\n------------------------------------------------")

# Calcula la cabeza del sistema
def Hs(pressure_1, pressure_2, density_1, velocity_1, velocity_2,
       z_1, z_2, frictions):
    dp = pressure_2-pressure_1
    dz = z_2-z_1
    dv = velocity_2**2-velocity_1**2
    return (dp*100**2)/(density_1) + (dz) + (dv)/(2*9.81) + frictions

# Calcula el número de Reynolds
def Re(velocity, diameter, density, viscosity):
    return velocity*diameter*density/viscosity

# Calcula los factores de fricción
def factor_friction(diameter, roughness, Reynolds):
    den = 0.25/(log10(1/(3.7*diameter/roughness)) + 5.74/Reynolds**0.9)**2
    return den

# Calcula las pérdidas de cabeza
def friction(f_friction, diameter, velocity, length):
    return f_friction*length*velocity**2/(diameter*2*9.81)

# Ayuda a grafica cuando lista
def plot_data(x: list, y: list, z:list) -> None:
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Cabeza de la bomba')
    ax.plot(x, z, label ='Cabeza del sistema')
    ax.set(xlabel='Flujo [L/min]', ylabel='Cabeza [m]', title= 'Cabeza vs Flujo')
    ax.set_ylim(0, max(y)+max(y)*0.1)
    ax.grid()
    ax.legend()
    plt.show()

def plot_2_data(x: list, y: list, z: list, s, title_1, title_2) -> None:
    fig, axs = plt.subplots(1, 2)
    axs[0].plot(x, y, label='Cabeza de la bomba')
    axs[0].plot(x, s, label='Cabeza de la sistema')
    axs[0].set_title(title_1)
    axs[1].plot(x, z, label='Cabeza de la bomba')
    axs[1].plot(x, s, label='Cabeza de la sistema')
    axs[1].set_title(title_2)
    axs[0].set(xlabel='Flujo [L/min]', ylabel='Cabeza [m]', title='Cabeza vs Flujo')
    axs[1].set(xlabel='Flujo [L/min]', ylabel='Cabeza [m]', title='Cabeza vs Flujo')
    axs[0].set_ylim(0, max(y)+max(y)*0.1)
    axs[1].set_ylim(0, max(z)+max(z)*0.1)
    axs[0].grid()
    axs[1].grid()
    axs[0].legend()
    axs[1].legend()
    plt.show()


# Calcula las velocidades 
def velocity(flow, diameter):
    return flow/(3.1416*(diameter/2)**2)

# Calcula la longuitud equivalente de cada accesorio 
def len_eq(accesorios: dict[str, int], len:dict[str, int]) -> float:
    dict = {k: accesorios[k]*len[k] for k in accesorios}
    longuitudeseq = sum(dict.values())
    return longuitudeseq 

# Calculan la cabeza de cada bomba
def bomba1(flujo):
    cabeza = (-2e-6*flujo**3) - (0.0005*flujo**2) - (0.0131*flujo) + 28.214
    return cabeza
def bomba1c(flujo):
    cabeza = (-0.0004*flujo**2) - (0.0211*flujo) + 23.07
    return cabeza
def bomba3a(flujo):
    cabeza = (-0.0003*flujo**2) - (0.0571*flujo) + 20.06
    return cabeza

def find_intersections(x, y1, y2):
    intersections = []
    for i in range(1, len(x)):
        if (y1[i-1] - y2[i-1]) * (y1[i] - y2[i]) < 0:
            # Aproximamos el punto de intersección
            xi = x[i-1] - (x[i] - x[i-1]) * (y1[i-1] - y2[i-1]) / ((y1[i] - y2[i]) - (y1[i-1] - y2[i-1]))
            yi = y1[i-1] + (y1[i] - y1[i-1]) * (xi - x[i-1]) / (x[i] - x[i-1])
            intersections.append((xi, yi))
    return intersections