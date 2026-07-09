import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def dSdt(t,S,B):
    """
    Use fd seguido de C-TAB para generar la funcion con docstrings
    Define el sistema de ecuaciones diferenciales para el movimiento del proyectil
    con resistencia al aire
    Parametros:
        t (float): Tiempo
        S (list): Estado actual [x, vx, y, vy]
        B (float): Coeficiente de resistencia del aire. Varía desde 0.0 a 1.0
    Retorna:
        list: Derivadas [dx/dt, dvx/dt, dy/dt, dvy/dt]
    """
    x, vx, y, vy = S
    return [vx,
            -B*np.sqrt(vx**2+vy**2)*vx,
            vy,
            -1-B*np.sqrt(vx**2+vy**2)*vy]

def resolver_trayectorias(V, B, tmax, angulos):
    """
    Resuelve las EDOs para múltiples ángulos de lanzamiento. Esto permite la simulación
    de varios lanzamientos con la misma velocidad inicial y coeficiente de resistencia
    del aire, pero en diferentes angulos de inclinación.
    
    Parámetros:
        V (float): Velocidad inicial.
        B (float): Coeficiente de resistencia del aire.
        tmax (float): Tiempo máximo de vuelo.
        angulos (list): Lista de ángulos en radianes.
        
    Retorna:
        list: Una lista con los objetos de solución devueltos por solve_ivp.
    """
    # Esta lista almacenará las soluciones devueltas por solve_ivp.
    soluciones = []
    
    for angulo in angulos:
        
        y0=[0,V*np.cos(angulo),0,V*np.sin(angulo)]
        
        solucion_actual=solve_ivp(dSdt,
                                  [0, tmax],
                                  y0,
                                  t_eval=np.linspace(0,tmax,1000), 
                                  args=(B,))       
        soluciones.append(solucion_actual)        

    return soluciones

def graficar_trayectoria(S, angulos):
    """
    Genera las curvas de trayectoria en un gráfico 2D y lo guarda en disco.

    Parámetros:
        S (list): Lista de soluciones de las EDOs devueltas por solve_ivp.
        angulos (list): Lista de ángulos correspondientes en radianes.
    """
    # Se crea el lienzo con su tamaño respectivo
    plt.figure(figsize=(9, 6))

    for solucion, angulo in zip(S, angulos):
        x = solucion.y[0]
        y = solucion.y[2]
        angulo_deg = angulo * 180 / np.pi
        # Aplicamos cambios a las leyendas del grafico
        plt.plot(x, y, label=f"Lanzamiento a {angulo_deg:.0f}°", linewidth=2)

    plt.ylim(bottom=0)
    
    # Se coloca un titulo principal a la imagen 
    plt.title("Alcance del Cohete según Ángulo de Lanzamiento", fontsize=16, fontweight='bold', pad=15)
    
    # Se hace ajustes a la leyenda del grafico 
    plt.legend(fontsize=12, loc='upper right')
    
    # Se bajo el tamaño de la letra de las leyendas de los ejes
    plt.xlabel('Distancia Horizontal ($x/g$)', fontsize=14)
    plt.ylabel('Altura ($y/g$)', fontsize=14)
    
    # Se agranda los numeros de los ejes para mejor visualizacion
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    
    # Se agregó un estilo a la cuadrícula
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Ajusta los bordes de forma automatica
    plt.tight_layout()
    
    # Se guarda la imagen
    plt.savefig("imagenes/trayectoria_cohete.png", dpi=300)
