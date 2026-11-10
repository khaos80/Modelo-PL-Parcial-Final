
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QApplication
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)

from matplotlib.figure import Figure


class GraficoView(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Método Gráfico - Programación Lineal"
        )

        self.resize(1500, 900)

        self.figure = Figure(
            figsize=(8, 6)
        )

        self.canvas = FigureCanvas(
            self.figure
        )

        self.inicializar_ui()

    # =======================================
    # FORMATEAR NÚMEROS
    # =======================================

    def formatear_numero(self, valor):

        try:

            numero = float(valor)

            if abs(numero - round(numero)) < 0.000001:

                return str(int(round(numero)))

            return str(round(numero, 4))

        except Exception:

            return str(valor)

    # =======================================
    # INTERFAZ
    # =======================================

    def inicializar_ui(self):

        layout_principal = QVBoxLayout()

        # ===================================
        # CABECERA
        # ===================================

        self.lbl_titulo = QLabel(
            "MÉTODO GRÁFICO - PROGRAMACIÓN LINEAL"
        )

        self.lbl_titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.lbl_titulo.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            color: white;
            background-color: #1B2A49;
            padding: 10px;
            border-radius: 8px;
            """
        )

        # ===================================
        # PANEL CENTRAL
        # ===================================

        contenido = QHBoxLayout()

        # ===================================
        # IZQUIERDA - GRÁFICA
        # ===================================

        grupo_grafica = QGroupBox(
            "Región Factible y Restricciones"
        )

        layout_grafica = QVBoxLayout()

        layout_grafica.addWidget(
            self.canvas
        )

        grupo_grafica.setLayout(
            layout_grafica
        )

        # ===================================
        # DERECHA
        # ===================================

        panel_derecho = QVBoxLayout()

        # -----------------------------------
        # RESULTADO DE OPTIMIZACIÓN
        # -----------------------------------

        grupo_resultado = QGroupBox(
            "Resultado de Optimización"
        )

        resultado_layout = QVBoxLayout()

        # Resultado principal

        self.lbl_z = QLabel(
            "🏆 Punto Óptimo\n\nZ = 0"
        )

        self.lbl_z.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.lbl_z.setMinimumHeight(145)

        self.lbl_z.setStyleSheet(
            """
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #0B5E20;
                background-color: #E8F5E9;
                border: 1px solid #A5D6A7;
                border-radius: 8px;
                padding: 10px;
            }
            """
        )

        # -----------------------------------
        # COORDENADAS X E Y
        # -----------------------------------

        coordenadas_layout = QHBoxLayout()

        self.lbl_x = QLabel(
            "X = 0"
        )

        self.lbl_y = QLabel(
            "Y = 0"
        )

        for etiqueta in [self.lbl_x, self.lbl_y]:

            etiqueta.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            etiqueta.setMinimumHeight(38)

            etiqueta.setStyleSheet(
                """
                QLabel {
                    font-size: 12px;
                    color: #1B5E20;
                    background-color: #E8F5E9;
                    border: 1px solid #A5D6A7;
                    border-radius: 6px;
                    padding: 5px;
                }
                """
            )

        coordenadas_layout.addWidget(
            self.lbl_x
        )

        coordenadas_layout.addWidget(
            self.lbl_y
        )

        # Agregar resultado y coordenadas

        resultado_layout.addWidget(
            self.lbl_z
        )

        resultado_layout.addLayout(
            coordenadas_layout
        )

        grupo_resultado.setLayout(
            resultado_layout
        )

        grupo_resultado.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                color: #0B5E20;
            }
            """
        )

        # -----------------------------------
        # EVALUACIÓN DE VÉRTICES
        # -----------------------------------

        grupo_vertices = QGroupBox(
            "Evaluación de Vértices"
        )

        vertices_layout = QVBoxLayout()

        self.tbl_vertices = QTableWidget()

        self.tbl_vertices.setColumnCount(2)

        self.tbl_vertices.setHorizontalHeaderLabels(
            [
                "Punto",
                "Valor Z"
            ]
        )

        self.tbl_vertices.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        vertices_layout.addWidget(
            self.tbl_vertices
        )

        grupo_vertices.setLayout(
            vertices_layout
        )

        # -----------------------------------
        # ESTADO DE RESTRICCIONES
        # -----------------------------------

        grupo_restricciones = QGroupBox(
            "Estado de Restricciones"
        )

        restricciones_layout = QVBoxLayout()

        self.tbl_restricciones = QTableWidget()

        self.tbl_restricciones.setColumnCount(3)

        self.tbl_restricciones.setHorizontalHeaderLabels(
            [
                "Restricción",
                "Resultado",
                "Estado"
            ]
        )

        self.tbl_restricciones.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        restricciones_layout.addWidget(
            self.tbl_restricciones
        )

        grupo_restricciones.setLayout(
            restricciones_layout
        )

        # -----------------------------------
        # BOTÓN VOLVER AL RESUMEN
        # -----------------------------------

        self.btn_volver_resumen = QPushButton(
            "Volver al Resumen"
        )

        self.btn_volver_resumen.setStyleSheet(
            """
            background: #1B2A49;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
            """
        )

        # -----------------------------------
        # BOTÓN SIMPLEX
        # -----------------------------------

        self.btn_simplex = QPushButton(
            "Mostrar Método Simplex"
        )

        self.btn_simplex.setStyleSheet(
            """
            background: #1B2A49;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
            """
        )

        # -----------------------------------
        # BOTÓN CERRAR
        # -----------------------------------

        self.btn_salir = QPushButton(
            "Cerrar Aplicación"
        )

        self.btn_salir.setStyleSheet(
            """
            padding: 10px;
            font-weight: bold;
            background: #E53935;
            color: white;
            border-radius: 6px;
            """
        )

        # -----------------------------------
        # ORGANIZAR PANEL DERECHO
        # -----------------------------------

        panel_derecho.addWidget(
            grupo_resultado
        )

        panel_derecho.addWidget(
            grupo_vertices
        )

        panel_derecho.addWidget(
            grupo_restricciones
        )

        panel_derecho.addWidget(
            self.btn_volver_resumen
        )

        panel_derecho.addWidget(
            self.btn_simplex
        )

        panel_derecho.addWidget(
            self.btn_salir
        )

        self.btn_salir.clicked.connect(
            self.cerrar_programa
        )

        # -----------------------------------
        # ORGANIZAR PANEL CENTRAL
        # -----------------------------------

        contenido.addWidget(
            grupo_grafica,
            2
        )

        contenido.addLayout(
            panel_derecho,
            1
        )

        layout_principal.addWidget(
            self.lbl_titulo
        )

        layout_principal.addLayout(
            contenido
        )

        self.setLayout(
            layout_principal
        )

    # =======================================
    # RESULTADO ÓPTIMO
    # =======================================

    def cargar_resultado(
        self,
        variables_optimas,
        valor_optimo
    ):

        # Actualizar valor Z

        self.lbl_z.setText(
            f"🏆 Punto Óptimo\n\n"
            f"Z = {self.formatear_numero(valor_optimo)}"
        )

        simbolos = list(
            variables_optimas.keys()
        )

        # Actualizar coordenada X

        if len(simbolos) >= 1:

            simbolo_x = simbolos[0]

            self.lbl_x.setText(
                f"{simbolo_x} = "
                f"{self.formatear_numero(variables_optimas[simbolo_x])}"
            )

        # Actualizar coordenada Y

        if len(simbolos) >= 2:

            simbolo_y = simbolos[1]

            self.lbl_y.setText(
                f"{simbolo_y} = "
                f"{self.formatear_numero(variables_optimas[simbolo_y])}"
            )

    # =======================================
    # EVALUACIÓN DE VÉRTICES
    # =======================================

    def cargar_vertices(
        self,
        evaluaciones,
        tipo_objetivo
    ):

        self.tbl_vertices.setRowCount(
            len(evaluaciones)
        )

        # Determinar el mejor valor Z

        if not evaluaciones:
            return

        if tipo_objetivo == "MAX":

            mejor_z = max(
                dato["z"]
                for dato in evaluaciones
            )

        else:

            mejor_z = min(
                dato["z"]
                for dato in evaluaciones
            )

        # Identificar vértices óptimos

        filas_optimas = []

        for fila, dato in enumerate(evaluaciones):

            if abs(dato["z"] - mejor_z) < 0.000001:

                filas_optimas.append(fila)

        # Cargar tabla

        for fila, dato in enumerate(evaluaciones):

            punto = dato["punto"]

            texto_punto = (
                f"({self.formatear_numero(punto[0])}, "
                f"{self.formatear_numero(punto[1])})"
            )

            item_punto = QTableWidgetItem(
                texto_punto
            )

            item_z = QTableWidgetItem(
                self.formatear_numero(dato["z"])
            )

            self.tbl_vertices.setItem(
                fila,
                0,
                item_punto
            )

            self.tbl_vertices.setItem(
                fila,
                1,
                item_z
            )

            # Resaltar vértices óptimos

            if fila in filas_optimas:

                for item in [item_punto, item_z]:

                    item.setBackground(
                        QColor("#C8E6C9")
                    )

                    item.setForeground(
                        QBrush(QColor("#000000"))
                    )

    # =======================================
    # ESTADO DE RESTRICCIONES
    # =======================================

    def cargar_restricciones(
        self,
        datos
    ):

        self.tbl_restricciones.setRowCount(
            len(datos)
        )

        for fila, restriccion in enumerate(datos):

            item_r = QTableWidgetItem(
                restriccion["restriccion"]
            )

            texto = (
                f"{self.formatear_numero(restriccion['valor'])} "
                f"{restriccion['signo']} "
                f"{self.formatear_numero(restriccion['limite'])}"
            )

            item_resultado = QTableWidgetItem(
                texto
            )

            cumple = restriccion["cumple"]

            estado = (
                "✅ Cumple"
                if cumple
                else "❌ No cumple"
            )

            item_estado = QTableWidgetItem(
                estado
            )

            color = (
                QColor("#C8E6C9")
                if cumple
                else QColor("#FFCDD2")
            )

            item_estado.setBackground(
                color
            )

            item_estado.setForeground(
                QBrush(QColor("black"))
            )

            self.tbl_restricciones.setItem(
                fila,
                0,
                item_r
            )

            self.tbl_restricciones.setItem(
                fila,
                1,
                item_resultado
            )

            self.tbl_restricciones.setItem(
                fila,
                2,
                item_estado
            )

    # =======================================
    # GRÁFICA BASE
    # =======================================

    def limpiar_grafica(self):

        self.figure.clear()

        self.ax = self.figure.add_subplot(
            111
        )

        self.ax.grid(True)

        self.ax.set_xlabel(
            "X"
        )

        self.ax.set_ylabel(
            "Y"
        )

        self.ax.set_title(
            "Método Gráfico"
        )

        self.canvas.draw()

    # =======================================
    # CERRAR APLICACIÓN
    # =======================================

    def cerrar_programa(self):

        respuesta = QMessageBox.question(
            self,
            "Cerrar Programa",
            "¿Desea cerrar completamente la aplicación?",
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:

            QApplication.instance().quit()
