import matplotlib.pyplot as plt
from math import log10


def Hb(pressure_1, pressure_2, density_1):
    (pressure_2-pressure_1)/(density_1*9.81)


def Hs(pressure_1, pressure_2, density_1, velocity_1, velocity_2,
       z_1, z_2, frictions):
    dp = pressure_2-pressure_1
    dz = z_2-z_1
    dv = velocity_2**2-velocity_1**2
    return (dp)/(density_1*9.81) + (dz) + (dv)/(2*9.81) + frictions


def Re(velocity, diameter, density, viscosity):
    return velocity*diameter*density/viscosity


def factor_friction(diameter, roughness, Reynolds):
    den = log10(1/(3.7*diameter/roughness) + 5.74/(Reynolds**0.9))
    return 0.25/(den**2)


def plot_data(x: list, y: list, title: str, xlabel: str, ylabel: str) -> None:
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.grid()
    plt.show()
