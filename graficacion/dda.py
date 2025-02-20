import matplotlib.pyplot as plt

def dda_line(x1, y1, x2, y2):
    # Calcular diferencias
    dx = x2 - x1
    dy = y2 - y1
    
    # Determinar el número de pasos
    steps = max(abs(dx), abs(dy))
    
    # Incrementos en cada eje
    x_inc = dx / steps
    y_inc = dy / steps
    
    # Listas para almacenar los puntos
    x_values = []
    y_values = []
    
    # Inicializar las coordenadas
    x, y = x1, y1
    for _ in range(steps + 1):
        x_values.append(round(x))
        y_values.append(round(y))
        x += x_inc
        y += y_inc
    
    return x_values, y_values

# Solicitar puntos de la línea al usuario
x1 = int(input("Ingrese la coordenada x1: "))
y1 = int(input("Ingrese la coordenada y1: "))
x2 = int(input("Ingrese la coordenada x2: "))
y2 = int(input("Ingrese la coordenada y2: "))

# Obtener los puntos de la línea
x_points, y_points = dda_line(x1, y1, x2, y2)

# Graficar la línea
plt.plot(x_points, y_points, marker='o', color='b', linestyle='-')
plt.grid(True)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Línea DDA")
plt.show()












