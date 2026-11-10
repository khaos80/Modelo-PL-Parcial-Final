from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QApplication
)

from PyQt6.QtGui import QColor, QBrush

from PyQt6.QtCore import Qt


class SimplexView(QWidget):

    def __init__(self):

        super().__init__()

        self.resultado = None

        self.iteracion_actual = 0

        self.setWindowTitle(
            "Método Simplex"
        )

        self.resize(
            1400,
            850
        )

        self.inicializar_ui()

    # ==================================================
    # UI
    # ==================================================

    def inicializar_ui(self):

        self.setStyleSheet("""

            QWidget{
                background:#222831;
                color:white;
                font-family:Segoe UI;
            }

            QGroupBox{
                border:1px solid #3A4750;
                border-radius:10px;
                margin-top:10px;
                padding-top:12px;
                font-weight:bold;
            }

            QGroupBox::title{
                color:#8CC8FF;
                left:10px;
                padding:2px 6px;
            }

            QTableWidget{
                background:#2D343F;
                gridline-color:#3A4750;
            }

            QHeaderView::section{
                background:#1B2A49;
                color:white;
                font-weight:bold;
                border:none;
                padding:6px;
            }

            QPushButton{
                background:#1B2A49;
                color:white;
                border:none;
                border-radius:8px;
                padding:10px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#28457D;
            }

        """)

        layout_principal = QVBoxLayout()

        # ==================================
        # CABECERA
        # ==================================

        self.lbl_titulo = QLabel(
            "MÉTODO SIMPLEX"
        )

        self.lbl_titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.lbl_titulo.setStyleSheet("""
            background:#1B2A49;
            border-radius:10px;
            padding:12px;
            font-size:22px;
            font-weight:bold;
        """)

        layout_principal.addWidget(
            self.lbl_titulo
        )

        # ==================================
        # INFO
        # ==================================

        grupo_info = QGroupBox(
            "Información de la Iteración"
        )

        info_layout = QGridLayout()

        self.lbl_iteracion = QLabel(
            "Iteración 0"
        )

        self.lbl_entrante = QLabel(
            "Variable Entrante: -"
        )

        self.lbl_saliente = QLabel(
            "Variable Saliente: -"
        )

        self.lbl_pivote = QLabel(
            "Pivote: -"
        )

        info_layout.addWidget(
            self.lbl_iteracion,
            0,
            0,
            1,
            2
        )

        info_layout.addWidget(
            self.lbl_entrante,
            1,
            0
        )

        info_layout.addWidget(
            self.lbl_saliente,
            1,
            1
        )

        info_layout.addWidget(
            self.lbl_pivote,
            2,
            0
        )

        grupo_info.setLayout(
            info_layout
        )

        layout_principal.addWidget(
            grupo_info
        )

        # ==================================
        # TABLA SIMPLEX
        # ==================================

        grupo_tabla = QGroupBox(
            "Tabla Simplex"
        )

        tabla_layout = QVBoxLayout()

        self.tbl_simplex = QTableWidget()

        self.tbl_simplex.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        tabla_layout.addWidget(
            self.tbl_simplex
        )

        grupo_tabla.setLayout(
            tabla_layout
        )

        layout_principal.addWidget(
            grupo_tabla
        )

        # ==================================
        # RESULTADO
        # ==================================

        grupo_resultado = QGroupBox(
            "Resultado Actual"
        )

        resultado_layout = QVBoxLayout()

        self.lbl_resultado = QLabel(
            "Sin solución disponible"
        )

        self.lbl_resultado.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#81C784;
            padding:10px;
        """)

        resultado_layout.addWidget(
            self.lbl_resultado
        )

        grupo_resultado.setLayout(
            resultado_layout
        )

        layout_principal.addWidget(
            grupo_resultado
        )

        # ==================================
        # BOTONES
        # ==================================

        botones = QHBoxLayout()

        self.btn_anterior = QPushButton(
            "← Iteración Anterior"
        )

        self.btn_siguiente = QPushButton(
            "Iteración Siguiente →"
        )

        self.btn_grafico = QPushButton(
            "Mostrar Método Gráfico"
        )

        self.btn_resumen = QPushButton(
            "Volver al Resumen"
        )

        self.btn_salir = QPushButton(
            "cerrar Aplicación"
        )

        self.btn_salir.setStyleSheet(
            """
            padding:10px;
            font-weight:bold;
            background:#E53935;
            color:white;
            border-radius:6px;
            """
        )

        botones.addWidget(
            self.btn_anterior
        )

        botones.addWidget(
            self.btn_siguiente
        )

        botones.addWidget(
            self.btn_grafico
        )

        botones.addWidget(
            self.btn_resumen
        )

        botones.addWidget(
            self.btn_salir
        )

        self.btn_salir.clicked.connect(
            self.cerrar_programa
        )

        layout_principal.addLayout(
            botones
        )

        self.setLayout(
            layout_principal
        )

    def formatear_numero(self, valor):

        try:

            numero = float(valor)

            if abs(
                numero - round(numero)
            ) < 0.000001:

                return str(
                    int(
                        round(numero)
                    )
                )

            return str(
                round(
                    numero,
                    4
                )
            )

        except Exception:

            return str(valor)

    # ==================================================
    # CARGAR RESULTADO
    # ==================================================

    def cargar_resultado(
        self,
        resultado
    ):

        self.resultado = resultado

        self.iteracion_actual = 0

        self.mostrar_iteracion()

    # ==================================================
    # MOSTRAR ITERACIÓN
    # ==================================================

    def mostrar_iteracion(self):

        if not self.resultado:

            return

        iteracion = (
            self.resultado["iteraciones"][
                self.iteracion_actual
            ]
        )

        tabla = iteracion["tabla"]

        variables = iteracion["variables"]

        base = iteracion["base"]

        fila_pivote = iteracion["fila_pivote"]

        columna_pivote = iteracion["columna_pivote"]

        # ------------------------------
        # CABECERAS
        # ------------------------------

        headers = (
            ["BV"]
            + variables
            + ["RHS"]
        )

        filas = len(tabla)

        columnas = len(headers)

        self.tbl_simplex.setRowCount(
            filas
        )

        self.tbl_simplex.setColumnCount(
            columnas
        )

        self.tbl_simplex.setHorizontalHeaderLabels(
            headers
        )

        # ------------------------------
        # CARGAR TABLA
        # ------------------------------

        for fila in range(filas):

            if fila < len(base):

                self.tbl_simplex.setItem(
                    fila,
                    0,
                    QTableWidgetItem(
                        str(base[fila])
                    )
                )

            else:

                self.tbl_simplex.setItem(
                    fila,
                    0,
                    QTableWidgetItem("Z")
                )

            for columna in range(
                len(tabla[fila])
            ):

                texto = self.formatear_numero(
                    tabla[fila][columna]
                )

                item = QTableWidgetItem(
                    texto
                )

                # Columna pivote

                if (
                    columna_pivote is not None
                    and
                    columna == columna_pivote
                ):

                    item.setBackground(
                        QColor("#BBDEFB")
                    )

                    item.setForeground(
                        QBrush(
                            QColor("#000000")
                        )
                    )

                # Fila pivote

                if (
                    fila_pivote is not None
                    and
                    fila == fila_pivote
                ):

                    item.setBackground(
                        QColor("#FFE080")
                    )

                    item.setForeground(
                        QBrush(
                            QColor("#000000")
                        )
                    )

                # Pivote

                if (
                    fila_pivote is not None
                    and
                    columna_pivote is not None
                    and
                    fila == fila_pivote
                    and
                    columna == columna_pivote
                ):

                    item.setBackground(
                        QColor("#81C784")
                    )

                    item.setForeground(
                        QBrush(
                            QColor("#000000")
                        )
                    )

                self.tbl_simplex.setItem(
                    fila,
                    columna + 1,
                    item
                )

        # ------------------------------
        # DATOS ITERACIÓN
        # ------------------------------

        total = len(
            self.resultado["iteraciones"]
        )

        if self.iteracion_actual == 0:

            self.lbl_iteracion.setText(
                "Tabla Inicial"
            )

        else:

            self.lbl_iteracion.setText(
                f"Iteración {self.iteracion_actual} de {total - 1}"
            ) 

        entrante = iteracion.get("variable_entrante")
        saliente = iteracion.get("variable_saliente")
        pivote = iteracion.get("pivote")

        self.lbl_entrante.setText(
            f"Variable Entrante: {entrante if entrante else '-'}"
        )

        self.lbl_saliente.setText(
            f"Variable Saliente: {saliente if saliente else '-'}"
        )

        self.lbl_pivote.setText(
            f"Pivote: {self.formatear_numero(pivote) if pivote is not None else '-'}"
        )

        # ------------------------------
        # RESULTADO FINAL
        # ------------------------------

        if (
            self.iteracion_actual
            ==
            total - 1
        ):

            solucion = (
                self.resultado.get(
                    "solucion",
                    {}
                )
            )

            texto = []

            for variable, valor in solucion.items():

                valor_texto = self.formatear_numero(
                    valor
                )

                texto.append(
                    f"{variable} = {valor_texto}"
                )

            texto.append(
                ""
            )

            if self.resultado.get("estado") == "OPTIMO":

                valor_z = self.formatear_numero(
                    self.resultado["valor_optimo"]
                )

                if float(valor_z).is_integer():

                    valor_z = int(valor_z)

                else:

                    valor_z = round(
                        valor_z,
                        4
                    )

                texto.append(
                    f"Z = {valor_z}"
                )

            self.lbl_resultado.setText(
                "\n".join(texto)
            )

        else:

            self.lbl_resultado.setText(
                "Avance del algoritmo..."
            )

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