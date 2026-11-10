from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QScrollArea,
    QHeaderView,
    QLineEdit
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QColor, QBrush

from PyQt6.QtWidgets import QAbstractItemView



class CapturaView(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Captura de Modelo"
        )

        self.resize(
            1200,
            850
        )

        self.setStyleSheet("""

            QWidget{
                background-color:#222831;
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
                subcontrol-origin: margin;
                left:10px;
                padding:2px 6px;
            }

            QLineEdit,
            QSpinBox,
            QComboBox{

                background:#2D343F;
                border:1px solid #3A4750;
                border-radius:5px;
                padding:6px;
                color:white;
            }

            QTableWidget{

                background:#2D343F;
                gridline-color:#3A4750;
            }

            QHeaderView::section{

                background:#1B2A49;
                color:white;
                padding:6px;
                font-weight:bold;
                border:none;
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

        self.inicializar_ui()

    def inicializar_ui(self):

        principal = QVBoxLayout()

        # ==================================
        # CABECERA
        # ==================================

        titulo = QLabel(
            "FORMULACIÓN DEL MODELO"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setStyleSheet("""

            background:#1B2A49;
            border-radius:10px;
            font-size:22px;
            font-weight:bold;
            padding:12px;
        """)

        principal.addWidget(
            titulo
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        contenido = QWidget()

        layout = QVBoxLayout()

        # ==================================
        # DATOS GENERALES
        # ==================================

        grupo_datos = QGroupBox(
            "Datos Generales"
        )

        datos_layout = QVBoxLayout()

        self.txt_nombre = QLineEdit()

        self.cmb_objetivo = QComboBox()

        self.cmb_objetivo.addItems(
            [
                "MAX",
                "MIN"
            ]
        )

        self.spn_variables = QSpinBox()

        self.spn_variables.setMinimum(2)
        self.spn_variables.setMaximum(5)

        datos_layout.addWidget(
            QLabel("Nombre del Problema")
        )

        datos_layout.addWidget(
            self.txt_nombre
        )

        datos_layout.addWidget(
            QLabel("Tipo de Objetivo")
        )

        datos_layout.addWidget(
            self.cmb_objetivo
        )

        datos_layout.addWidget(
            QLabel("Cantidad de Variables")
        )

        datos_layout.addWidget(
            self.spn_variables
        )

        grupo_datos.setLayout(
            datos_layout
        )

        # ==================================
        # VARIABLES
        # ==================================

        grupo_variables = QGroupBox(
            "Variables de Decisión"
        )

        variables_layout = QVBoxLayout()

        self.tbl_variables = QTableWidget(
            2,
            2
        )

        self.tbl_variables.setEditTriggers(
            QAbstractItemView.EditTrigger.CurrentChanged
        )

        self.tbl_variables.setHorizontalHeaderLabels(
            [
                "Variable",
                "Descripción"
            ]
        )

        self.tbl_variables.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.tbl_variables.setColumnWidth(
            0,
            120
        )

        self.tbl_variables.horizontalHeader().setStretchLastSection(
            True
        )

        variables_layout.addWidget(
            self.tbl_variables
        )

        grupo_variables.setLayout(
            variables_layout
        )

        # ==================================
        # FUNCIÓN OBJETIVO
        # ==================================

        grupo_objetivo = QGroupBox(
            "Función Objetivo"
        )

        objetivo_layout = QVBoxLayout()

        etiqueta_obj = QLabel(
            "Coeficientes de la Función Objetivo"
        )

        self.tbl_objetivo = QTableWidget(
            1,
            2
        )

        self.tbl_objetivo.setEditTriggers(
            QAbstractItemView.EditTrigger.CurrentChanged
        )

        self.tbl_objetivo.setHorizontalHeaderLabels(
            [
                "X",
                "Y"
            ]
        )

        objetivo_layout.addWidget(
            etiqueta_obj
        )

        objetivo_layout.addWidget(
            self.tbl_objetivo
        )

        grupo_objetivo.setLayout(
            objetivo_layout
        )

        # ==================================
        # RESTRICCIONES
        # ==================================

        grupo_restricciones = QGroupBox(
            "Restricciones del Modelo"
        )

        restricciones_layout = QVBoxLayout()

        self.tbl_restricciones = QTableWidget(
            2,
            4
        )

        self.tbl_restricciones.setEditTriggers(
            QAbstractItemView.EditTrigger.CurrentChanged
        )

        self.tbl_restricciones.setHorizontalHeaderLabels(
            [
                "Coef X",
                "Coef Y",
                "Relación",
                "Límite"
            ]
        )

        restricciones_layout.addWidget(
            self.tbl_restricciones
        )

        botones_restricciones = QHBoxLayout()

        self.btn_agregar = QPushButton(
            "Agregar Restricción"
        )

        self.btn_eliminar = QPushButton(
            "Eliminar Restricción"
        )

        botones_restricciones.addWidget(
            self.btn_agregar
        )

        botones_restricciones.addWidget(
            self.btn_eliminar
        )

        restricciones_layout.addLayout(
            botones_restricciones
        )

        grupo_restricciones.setLayout(
            restricciones_layout
        )

        # ==================================
        # BOTON PRINCIPAL
        # ==================================

        self.btn_resumen = QPushButton(
            "GENERAR RESUMEN"
        )

        self.btn_resumen.setMinimumHeight(
            55
        )

        self.btn_resumen.setStyleSheet("""

            QPushButton{

                background:#0B5E20;
                color:white;
                font-size:14px;
                font-weight:bold;
                border-radius:8px;
            }

            QPushButton:hover{

                background:#087F23;
            }
        """)

        # ==================================
        # AGREGAR AL LAYOUT
        # ==================================

        layout.addWidget(
            grupo_datos
        )

        layout.addWidget(
            grupo_variables
        )

        layout.addWidget(
            grupo_objetivo
        )

        layout.addWidget(
            grupo_restricciones
        )

        layout.addWidget(
            self.btn_resumen
        )

        contenido.setLayout(
            layout
        )

        scroll.setWidget(
            contenido
        )

        principal.addWidget(
            scroll
        )

        self.setLayout(
            principal
        )

        # ==================================
        # EVENTOS
        # ==================================

        self.spn_variables.valueChanged.connect(
            self.actualizar_variables
        )

        self.btn_agregar.clicked.connect(
            self.agregar_restriccion
        )

        self.btn_eliminar.clicked.connect(
            self.eliminar_restriccion
        )

        self.tbl_variables.setMinimumHeight(
            180
        )

        self.tbl_objetivo.setMinimumHeight(
            70
        )

        self.tbl_restricciones.setMinimumHeight(
            180
        )

        self.actualizar_variables()

        self.configurar_signos()

    def actualizar_variables(self):

        simbolos = [
            "X",
            "Y",
            "Z",
            "W",
            "V"
        ]

        cantidad = self.spn_variables.value()

        # -------------------------
        # Variables
        # -------------------------

        self.tbl_variables.clearContents()
        self.tbl_variables.setRowCount(cantidad)

        for fila in range(cantidad):

            item = QTableWidgetItem(
                simbolos[fila]
            )

            item.setFlags(
                item.flags()
                &
                ~Qt.ItemFlag.ItemIsEditable
            )

            item.setBackground(
                QColor("#E0E0E0")
            )

            item.setForeground(
                QBrush(
                    QColor("#000000")
                )
            )

            self.tbl_variables.setItem(
                fila,
                0,
                item
            )

        self.tbl_variables.verticalHeader().setVisible(
            True
        )

        for fila in range(cantidad):

            self.tbl_variables.setVerticalHeaderItem(
                fila,
                QTableWidgetItem(
                    str(fila + 1)
                )
            )

        self.tbl_variables.horizontalHeader(
        ).setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.tbl_variables.horizontalHeader(
        ).setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )

        # -------------------------
        # Función objetivo
        # -------------------------

        self.tbl_objetivo.clearContents()

        self.tbl_objetivo.setColumnCount(
            cantidad
        )

        self.tbl_objetivo.setHorizontalHeaderLabels(
            simbolos[:cantidad]
        )

        self.tbl_objetivo.verticalHeader().setVisible(
            False
        )

        self.tbl_objetivo.horizontalHeader(
        ).setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # -------------------------
        # Restricciones
        # -------------------------

        self.actualizar_restricciones()

    def actualizar_restricciones(self):

        cantidad_variables = (
            self.spn_variables.value()
        )

        filas = self.tbl_restricciones.rowCount()

        self.tbl_restricciones.clearContents()

        self.tbl_restricciones.setRowCount(
            filas
        )

        columnas = (
            cantidad_variables + 2
        )

        self.tbl_restricciones.setColumnCount(
            columnas
        )

        headers = (
            ["X", "Y", "Z", "W", "V"][
                :cantidad_variables
            ]
            +
            [
                "Relación",
                "Límite"
            ]
        )

        self.tbl_restricciones.setHorizontalHeaderLabels(
            headers
        )

        self.tbl_restricciones.verticalHeader().setVisible(
            True
        )

        for fila in range(filas):

            self.tbl_restricciones.setVerticalHeaderItem(
                fila,
                QTableWidgetItem(
                    str(fila + 1)
                )
            )

        self.tbl_restricciones.horizontalHeader(
        ).setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tbl_restricciones.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.configurar_signos()

    def configurar_signos(self):

        columna_relacion = (
            self.spn_variables.value()
        )

        for fila in range(
            self.tbl_restricciones.rowCount()
        ):

            combo = QComboBox()

            combo.addItems(
                [
                    "",
                    "<=",
                    ">=",
                    "="
                ]
            )

            self.tbl_restricciones.setCellWidget(
                fila,
                columna_relacion,
                combo
            )

    def agregar_restriccion(self):

        fila = (
            self.tbl_restricciones.rowCount()
        )

        self.tbl_restricciones.insertRow(
            fila
        )

        self.tbl_restricciones.setVerticalHeaderItem(
            fila,
            QTableWidgetItem(
                str(fila + 1)
            )
        )

        columna_relacion = (
            self.spn_variables.value()
        )

        combo = QComboBox()

        combo.addItems(
            [
                "",
                "<=",
                ">=",
                "="
            ]
        )

        self.tbl_restricciones.setCellWidget(
            fila,
            columna_relacion,
            combo
        )

    def eliminar_restriccion(self):

        filas = (
            self.tbl_restricciones.rowCount()
        )

        if filas > 1:

            self.tbl_restricciones.removeRow(
                filas - 1
            )