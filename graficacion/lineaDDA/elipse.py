import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, \
    QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class EllipseDrawingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dibujar Elipse - Algoritmo de Punto Medio")
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        control_panel = QVBoxLayout()

        # Entradas
        input_group = QGroupBox("Centro y Radios")
        input_group.setFont(QFont("Arial", 10, QFont.Bold))
        grid = QGridLayout()

        grid.addWidget(QLabel("Centro X:"), 0, 0)
        self.x_center = QLineEdit()
        grid.addWidget(self.x_center, 0, 1)
        grid.addWidget(QLabel("Centro Y:"), 0, 2)
        self.y_center = QLineEdit()
        grid.addWidget(self.y_center, 0, 3)
        grid.addWidget(QLabel("Radio X:"), 1, 0)
        self.rx = QLineEdit()
        grid.addWidget(self.rx, 1, 1)
        grid.addWidget(QLabel("Radio Y:"), 1, 2)
        self.ry = QLineEdit()
        grid.addWidget(self.ry, 1, 3)

        input_group.setLayout(grid)
        control_panel.addWidget(input_group)

        # Botones
        button_layout = QHBoxLayout()
        self.draw_button = QPushButton("Dibujar")
        self.draw_button.setStyleSheet("background-color: lightblue;")
        self.draw_button.clicked.connect(self.draw_ellipse)
        button_layout.addWidget(self.draw_button)

        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet("background-color: lightcoral;")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)

        control_panel.addLayout(button_layout)

        # Tablas
        self.tables = {}
        labels = ["(Pk, X, Y)", "(X, -Y)", "(-X, -Y)", "(-X, Y)"]
        table_layout = QGridLayout()

        for i, label in enumerate(labels):
            group = QVBoxLayout()
            title = QLabel(f"Puntos {label}")
            title.setAlignment(Qt.AlignCenter)
            group.addWidget(title)
            table = QTableWidget()
            table.setColumnCount(3 if label == "(Pk, X, Y)" else 2)
            headers = ["Pk", "X", "Y"] if label == "(Pk, X, Y)" else label.replace("(", "").replace(")", "").split(", ")
            table.setHorizontalHeaderLabels(headers)
            table.setFixedHeight(250)
            table.setMinimumWidth(250)
            self.tables[label] = table
            group.addWidget(table)
            table_layout.addLayout(group, i // 2, i % 2)

        control_panel.addLayout(table_layout)

        # Gráfico
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout.addLayout(control_panel, 4)
        layout.addWidget(self.canvas, 5)
        self.setLayout(layout)

    def draw_ellipse(self):
        self.ax.clear()
        x_c = int(self.x_center.text())
        y_c = int(self.y_center.text())
        rx = int(self.rx.text())
        ry = int(self.ry.text())

        points = self.midpoint_ellipse(x_c, y_c, rx, ry)

        self.ax.set_aspect('equal')
        self.ax.set_xlim(x_c - rx - 10, x_c + rx + 10)
        self.ax.set_ylim(y_c - ry - 10, y_c + ry + 10)
        self.ax.grid(True, linestyle='--', alpha=0.6)

        for x, y in points:
            self.ax.plot(x, y, 'bo')

        self.canvas.draw()

    def midpoint_ellipse(self, xc, yc, rx, ry):
        x = 0
        y = ry
        rx2 = rx * rx
        ry2 = ry * ry
        tworx2 = 2 * rx2
        twory2 = 2 * ry2
        px = 0
        py = tworx2 * y
        points = []

        # Region 1
        p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
        while px < py:
            sym_points = self.plot_symmetry(x, y, xc, yc)
            points.extend(sym_points)
            self.update_tables(p1, x, y, sym_points)

            x += 1
            px += twory2
            if p1 < 0:
                p1 += ry2 + px
            else:
                y -= 1
                py -= tworx2
                p1 += ry2 + px - py

        # Region 2
        p2 = ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2
        while y >= 0:
            sym_points = self.plot_symmetry(x, y, xc, yc)
            points.extend(sym_points)
            self.update_tables(p2, x, y, sym_points)

            y -= 1
            py -= tworx2
            if p2 > 0:
                p2 += rx2 - py
            else:
                x += 1
                px += twory2
                p2 += rx2 - py + px

        return points

    def plot_symmetry(self, x, y, xc, yc):
        return [
            (xc + x, yc + y),  # original
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc - x, yc + y),
        ]

    def update_tables(self, p, x, y, sym_points):
        row = self.tables["(Pk, X, Y)"].rowCount()
        self.tables["(Pk, X, Y)"].insertRow(row)
        self.tables["(Pk, X, Y)"].setItem(row, 0, QTableWidgetItem(str(round(p, 2))))
        self.tables["(Pk, X, Y)"].setItem(row, 1, QTableWidgetItem(str(x)))
        self.tables["(Pk, X, Y)"].setItem(row, 2, QTableWidgetItem(str(y)))

        labels = ["(X, -Y)", "(-X, -Y)", "(-X, Y)"]
        for i, label in enumerate(labels):
            table = self.tables[label]
            r = table.rowCount()
            table.insertRow(r)
            table.setItem(r, 0, QTableWidgetItem(str(sym_points[i + 1][0])))
            table.setItem(r, 1, QTableWidgetItem(str(sym_points[i + 1][1])))

    def clear_all(self):
        self.ax.clear()
        self.canvas.draw()
        for table in self.tables.values():
            table.setRowCount(0)
        self.x_center.clear()
        self.y_center.clear()
        self.rx.clear()
        self.ry.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EllipseDrawingApp()
    window.show()
    sys.exit(app.exec_())
