import argparse
import numpy as np
from utils.projectile_functions import resolver_trayectorias
from utils.projectile_functions import graficar_trayectoria

def main():
    # Aplicando el snippet: pars
    parser = argparse.ArgumentParser(description='Simulación de trayectoria de cohete con resistencia al aire')

    # snippet: args (Repetir para cada parámetro)
    parser.add_argument("-v", type=float, required=True, help="Velocidad inicial (m/s)")
    parser.add_argument("-b", type=float, required=True, help="Coeficiente de fricción B")
    parser.add_argument("-t", type=float, required=True, help="Tiempo máximo de vuelo (s)")
    # 'nargs="+"' permite recibir una lista de valores para los ángulos
    parser.add_argument("-a", type=float, nargs="+", required=True, help="Lista de ángulos de lanzamiento en grados")
    args = parser.parse_args()

    # Convertimos los ángulos en grados a radianes 
    angulos_rad = [a * np.pi / 180 for a in args.a]

    # Se llama al motor de resolución
    soluciones = resolver_trayectorias(args.v, args.b, args.t, angulos_rad)

    # 3. Generar y guardar la gráfica
    graficar_trayectoria(soluciones, angulos_rad)
    
    print(f"Simulación finalizada. Imagen guardada en 'imagenes/trayectoria_cohete.png'")

# snippet: ifm
if __name__ == "__main__":
    main()







