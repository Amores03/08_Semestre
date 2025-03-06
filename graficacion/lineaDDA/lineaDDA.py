import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LineDrawingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generación de Triángulo - Algoritmo DDA")
        self.setGeometry(100, 100, 900, 600)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        control_panel = QVBoxLayout()
        
        # Contenedor de coordenadas
        coord_group = QGroupBox("Coordenadas")
        coord_group.setFont(QFont("Arial", 10, QFont.Bold))
        grid = QGridLayout()
        
        self.coord_inputs = {}
        for i, point in enumerate(['A', 'B', 'C']):
            grid.addWidget(QLabel(f"{point} X:"), i, 0)
            self.coord_inputs[f"x{point}"] = QLineEdit()
            grid.addWidget(self.coord_inputs[f"x{point}"], i, 1)
            grid.addWidget(QLabel(f"{point} Y:"), i, 2)
            self.coord_inputs[f"y{point}"] = QLineEdit()
            grid.addWidget(self.coord_inputs[f"y{point}"], i, 3)
        
        coord_group.setLayout(grid)
        control_panel.addWidget(coord_group)
        
        # Botones
        button_layout = QHBoxLayout()
        self.draw_button = QPushButton("Dibujar")
        self.draw_button.setStyleSheet("background-color: lightblue;")
        self.draw_button.clicked.connect(self.draw_triangle)
        button_layout.addWidget(self.draw_button)
        
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet("background-color: lightcoral;")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        control_panel.addLayout(button_layout)
        
        # Tablas
        self.tables = {}
        table_layout = QHBoxLayout()
        for label in ['A-B', 'B-C', 'C-A']:
            table_group = QVBoxLayout()
            table_title = QLabel(f"Puntos {label}")
            table_title.setAlignment(Qt.AlignCenter)
            table_group.addWidget(table_title)
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["X", "Y"])
            table.setFixedWidth(200)
            self.tables[label] = table
            table_group.addWidget(table)
            table_layout.addLayout(table_group)
        
        control_panel.addLayout(table_layout)
        
        # Información de pendiente
        self.slope_info = {}
        for label in ['A-B', 'B-C', 'C-A']:
            text_box = QTextEdit()
            text_box.setReadOnly(True)
            text_box.setFixedHeight(50)
            control_panel.addWidget(text_box)
            self.slope_info[label] = text_box
        
        # Gráfico
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        
        layout.addLayout(control_panel, 2)
        layout.addWidget(self.canvas, 5)
        self.setLayout(layout)
    
    def draw_triangle(self):
        self.ax.clear()
        points = [(int(self.coord_inputs[f"x{p}"].text()), int(self.coord_inputs[f"y{p}"].text())) for p in "ABC"]
        
        self.ax.fill([p[0] for p in points], [p[1] for p in points], 'cyan', alpha=0.5)
        self.update_tables(points)
        self.update_slopes(points)
        self.canvas.draw()
    
    def update_tables(self, points):
        for table, (p1, p2) in zip(self.tables.values(), [(0,1), (1,2), (2,0)]):
            table.setRowCount(0)
            x1, y1 = points[p1]
            x2, y2 = points[p2]
            dx, dy = x2 - x1, y2 - y1
            steps = max(abs(dx), abs(dy))
            x_inc, y_inc = dx / steps, dy / steps
            x, y = x1, y1
            for i in range(steps + 1):
                table.insertRow(i)
                table.setItem(i, 0, QTableWidgetItem(str(round(x))))
                table.setItem(i, 1, QTableWidgetItem(str(round(y))))
                x += x_inc
                y += y_inc
    
    def update_slopes(self, points):
        for (p1, p2), label in zip([(0,1), (1,2), (2,0)], ['A-B', 'B-C', 'C-A']):
            x1, y1 = points[p1]
            x2, y2 = points[p2]
            slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
            direction = "de izquierda a derecha" if x2 > x1 else "de derecha a izquierda"
            self.slope_info[label].setText(f"Pendiente y dirección de {label}:\nTiene una pendiente de {round(slope, 2)} y va {direction}")
    
    def clear_all(self):
        self.ax.clear()
        self.canvas.draw()
        for table in self.tables.values():
            table.setRowCount(0)
        for input_field in self.coord_inputs.values():
            input_field.clear()
        for text_box in self.slope_info.values():
            text_box.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LineDrawingApp()
    ex.show()
    sys.exit(app.exec_())