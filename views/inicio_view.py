from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame,
    QSizePolicy
)

from PyQt6.QtCore import Qt


class InicioView(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Programación Lineal"
        )

        self.resize(
            900,
            650
        )

        self.inicializar_ui()

    def inicializar_ui(self):

        self.setStyleSheet("""
            QWidget {
                background-color: #222831;
                color: white;
                font-family: Segoe UI;
            }

            QPushButton {
                background-color: #1B2A49;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #28457D;
            }

            QLabel {
                color: white;
            }
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            40,
            30,
            40,
            30
        )

        layout.setSpacing(
            15
        )

        # ======================================
        # CABECERA
        # ======================================

        cabecera = QLabel(
            "PROGRAMACIÓN LINEAL"
        )

        cabecera.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        cabecera.setStyleSheet("""
            background-color: #1B2A49;
            border-radius: 10px;
            padding: 15px;
            font-size: 24px;
            font-weight: bold;
        """)

        # ======================================
        # ICONO
        # ======================================

        icono = QLabel("📈")

        icono.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        icono.setStyleSheet("""
            font-size: 60px;
        """)

        # ======================================
        # TITULO
        # ======================================

        titulo = QLabel(
            "FORMULADOR DE MODELOS\nDE PROGRAMACIÓN LINEAL"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        # ======================================
        # DESCRIPCION
        # ======================================

        descripcion = QLabel(
            "Construya y resuelva modelos mediante\n"
            "Método Gráfico y Método Simplex"
        )

        descripcion.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descripcion.setStyleSheet("""
            font-size: 14px;
            color: #D6D6D6;
        """)

        # ======================================
        # SEPARADOR
        # ======================================

        linea = QFrame()

        linea.setFrameShape(
            QFrame.Shape.HLine
        )

        linea.setStyleSheet("""
            background:#3A4750;
        """)

        # ======================================
        # BOTONES
        # ======================================

        self.btn_crear = QPushButton(
            "Crear Modelo"
        )

        self.btn_instrucciones = QPushButton(
            "Instrucciones"
        )

        self.btn_salir = QPushButton(
            "Salir"
        )

        self.btn_crear.setMinimumHeight(
            55
        )

        self.btn_instrucciones.setMinimumHeight(
            55
        )

        self.btn_salir.setMinimumHeight(
            55
        )

        # ======================================
        # LAYOUT
        # ======================================

        layout.addWidget(
            cabecera
        )

        layout.addStretch()

        layout.addWidget(
            icono
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            descripcion
        )

        layout.addWidget(
            linea
        )

        layout.addSpacing(10)

        layout.addWidget(
            self.btn_crear
        )

        layout.addWidget(
            self.btn_instrucciones
        )

        layout.addWidget(
            self.btn_salir
        )

        layout.addStretch()

        self.setLayout(
            layout
        )