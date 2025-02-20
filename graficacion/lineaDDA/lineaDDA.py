import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def dda_algorithm(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    Xinc = dx / steps
    Yinc = dy / steps

    x, y = x1, y1
    for i in range(int(steps) + 1):
        points.append((x, y))  # Guardamos valores con decimales
        x += Xinc
        y += Yinc
    return points


def plot_line():
    x1 = float(entry_x1.get())
    y1 = float(entry_y1.get())
    x2 = float(entry_x2.get())
    y2 = float(entry_y2.get())

    points = dda_algorithm(x1, y1, x2, y2)

    # Limpiar tabla
    for row in tree.get_children():
        tree.delete(row)

    # Llenar tabla con valores decimales
    for i, (x, y) in enumerate(points):
        tree.insert("", "end", values=(i, f"{x:.2f}", f"{y:.2f}"))  # Formato con 2 decimales

    # Graficar línea
    ax.clear()
    ax.plot([p[0] for p in points], [p[1] for p in points], marker="o", color="b", linestyle="-")
    ax.set_xlim(min(x1, x2) - 1, max(x1, x2) + 1)
    ax.set_ylim(min(y1, y2) - 1, max(y1, y2) + 1)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    canvas.draw()


def clear_all():
    entry_x1.delete(0, tk.END)
    entry_y1.delete(0, tk.END)
    entry_x2.delete(0, tk.END)
    entry_y2.delete(0, tk.END)

    for row in tree.get_children():
        tree.delete(row)

    ax.clear()
    canvas.draw()


def clear_line():
    for row in tree.get_children():
        tree.delete(row)
    ax.clear()
    canvas.draw()


# Crear ventana principal
root = tk.Tk()
root.title("Algoritmo DDA - Generación de Líneas")
root.geometry("900x600")

# Sección principal
frame_main = tk.Frame(root)
frame_main.pack(side=tk.LEFT, padx=10, pady=10)

# Sección de entrada de coordenadas
frame_input = tk.Frame(frame_main)
frame_input.pack()

label_a = tk.Label(frame_input, text="Coordenadas A", font=("Arial", 10, "bold"))
label_a.grid(row=0, column=0, columnspan=2)

tk.Label(frame_input, text="X1:").grid(row=1, column=0)
tk.Label(frame_input, text="Y1:").grid(row=2, column=0)
entry_x1 = tk.Entry(frame_input, width=5)
entry_y1 = tk.Entry(frame_input, width=5)
entry_x1.grid(row=1, column=1)
entry_y1.grid(row=2, column=1)

label_b = tk.Label(frame_input, text="Coordenadas B", font=("Arial", 10, "bold"))
label_b.grid(row=3, column=0, columnspan=2)

tk.Label(frame_input, text="X2:").grid(row=4, column=0)
tk.Label(frame_input, text="Y2:").grid(row=5, column=0)
entry_x2 = tk.Entry(frame_input, width=5)
entry_y2 = tk.Entry(frame_input, width=5)
entry_x2.grid(row=4, column=1)
entry_y2.grid(row=5, column=1)

btn_generate = tk.Button(frame_input, text="Generar Línea", command=plot_line, bg="lightblue", font=("Arial", 10))
btn_generate.grid(row=6, column=0, columnspan=2, pady=5)

btn_clear = tk.Button(frame_input, text="Eliminar Todo", command=clear_all, bg="lightcoral", font=("Arial", 10))
btn_clear.grid(row=7, column=0, columnspan=2, pady=5)

btn_clear_line = tk.Button(frame_input, text="Borrar Línea", command=clear_line, bg="lightgray", font=("Arial", 10))
btn_clear_line.grid(row=8, column=0, columnspan=2, pady=5)

# Tabla de valores
frame_table = tk.Frame(frame_main)
frame_table.pack(pady=10)

tree = ttk.Treeview(frame_table, columns=("#", "X", "Y"), show="headings", height=5)
tree.column("#", width=30, anchor="center")
tree.column("X", width=50, anchor="center")
tree.column("Y", width=50, anchor="center")
tree.heading("#", text="#")
tree.heading("X", text="X")
tree.heading("Y", text="Y")
tree.pack()

# Sección de gráfica
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)

fig, ax = plt.subplots(figsize=(7, 7))
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

root.mainloop()



