import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CircleDrawingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dibujar Círculo - Algoritmo de Punto Medio")
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        control_panel = QVBoxLayout()
        
        # Contenedor de entrada
        coord_group = QGroupBox("Centro y Radio")
        coord_group.setFont(QFont("Arial", 10, QFont.Bold))
        grid = QGridLayout()
        
        grid.addWidget(QLabel("Centro X:"), 0, 0)
        self.x_center = QLineEdit()
        grid.addWidget(self.x_center, 0, 1)
        grid.addWidget(QLabel("Centro Y:"), 0, 2)
        self.y_center = QLineEdit()
        grid.addWidget(self.y_center, 0, 3)
        grid.addWidget(QLabel("Radio:"), 1, 0)
        self.radius = QLineEdit()
        grid.addWidget(self.radius, 1, 1)
        
        coord_group.setLayout(grid)
        control_panel.addWidget(coord_group)
        
        # Botones
        button_layout = QHBoxLayout()
        self.draw_button = QPushButton("Dibujar")
        self.draw_button.setStyleSheet("background-color: lightblue;")
        self.draw_button.clicked.connect(self.draw_circle)
        button_layout.addWidget(self.draw_button)
        
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet("background-color: lightcoral;")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        control_panel.addLayout(button_layout)
        
        # Tablas
        self.tables = {}
        table_layout = QGridLayout()
        labels = ["(Pk, X, Y)", "(Y, X)", "(-Y, X)", "(X, -Y)", "(-Y, -X)", "(-X, -Y)", "(-X, Y)", "(Y, -X)"]
        
        for i, label in enumerate(labels):
            table_group = QVBoxLayout()
            table_title = QLabel(f"Puntos {label}")
            table_title.setAlignment(Qt.AlignCenter)
            table_group.addWidget(table_title)
            table = QTableWidget()
            table.setColumnCount(3 if label == "(Pk, X, Y)" else 2)
            headers = ["Pk", "X", "Y"] if label == "(Pk, X, Y)" else label.replace("(", "").replace(")", "").split(", ")
            table.setHorizontalHeaderLabels(headers)
            table.setFixedHeight(250)  # Hace las tablas más largas
            table.setMinimumWidth(250)  # Ajusta el ancho
            self.tables[label] = table
            table_group.addWidget(table)
            table_layout.addLayout(table_group, i // 4, i % 4)
        
        control_panel.addLayout(table_layout)
        
        # Gráfico
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        
        layout.addLayout(control_panel, 4)
        layout.addWidget(self.canvas, 5)
        self.setLayout(layout)
    
    def draw_circle(self):
        self.ax.clear()
        x_c = int(self.x_center.text())
        y_c = int(self.y_center.text())
        r = int(self.radius.text())
        
        points = self.midpoint_circle(x_c, y_c, r)
        
        self.ax.set_aspect('equal')
        self.ax.set_xlim(x_c - r - 5, x_c + r + 5)
        self.ax.set_ylim(y_c - r - 5, y_c + r + 5)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        for x, y in points:
            self.ax.plot(x, y, 'bo')
        
        self.canvas.draw()
    
    def midpoint_circle(self, x_c, y_c, r):
        x, y = 0, r
        p = 1 - r
        points = []
        
        while x <= y:
            sym_points = [
                (x_c + x, y_c + y), (x_c + y, y_c + x),
                (x_c - y, y_c + x), (x_c - x, y_c + y),
                (x_c - x, y_c - y), (x_c - y, y_c - x),
                (x_c + y, y_c - x), (x_c + x, y_c - y)
            ]
            
            points.extend(sym_points)
            self.update_tables(p, x, y, sym_points)
            
            if p < 0:
                p += 2 * x + 3
            else:
                p += 2 * (x - y) + 5
                y -= 1
            x += 1
        
        return points
    
    def update_tables(self, p, x, y, sym_points):
        labels = ["(Pk, X, Y)", "(Y, X)", "(-Y, X)", "(X, -Y)", "(-Y, -X)", "(-X, -Y)", "(-X, Y)", "(Y, -X)"]
        
        row = self.tables["(Pk, X, Y)"].rowCount()
        self.tables["(Pk, X, Y)"].insertRow(row)
        self.tables["(Pk, X, Y)"].setItem(row, 0, QTableWidgetItem(str(p)))
        self.tables["(Pk, X, Y)"].setItem(row, 1, QTableWidgetItem(str(x)))
        self.tables["(Pk, X, Y)"].setItem(row, 2, QTableWidgetItem(str(y)))
        
        for i, label in enumerate(labels[1:]):
            table = self.tables[label]
            row_idx = table.rowCount()
            table.insertRow(row_idx)
            table.setItem(row_idx, 0, QTableWidgetItem(str(sym_points[i][0])))
            table.setItem(row_idx, 1, QTableWidgetItem(str(sym_points[i][1])))
    
    def clear_all(self):
        self.ax.clear()
        self.canvas.draw()
        
        for table in self.tables.values():
            table.setRowCount(0)
        
        self.x_center.clear()
        self.y_center.clear()
        self.radius.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CircleDrawingApp()
    ex.show()
    sys.exit(app.exec_())
