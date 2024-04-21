import time

#conseguir información del sistema del usuario 
def get_info():
    print("¡Bienvenido, aquí podrás elegir la mejor bomba para tu proceso!")
    time.sleep(1.5)
    print("Por favor ingresa los requerimientos y características de tu proceso.")
    while True:
        try: 
            h = float(input("Ingresa la cabeza que necesita tu proceso: "))
            q = float(input("Ingresa el flujo que necesita tu proceso: "))
            break
        except ValueError:
            print("Solo se admmiten números, inténtelo de nuevo.")

get_info()   

