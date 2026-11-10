from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGroupBox,
    QTextEdit,
    QMessageBox,
    QApplication
)

from PyQt6.QtCore import Qt


class ResumenView(QWidget):

    def __init__(self, problema):

        super().__init__()

        self.problema = problema

        self.setWindowTitle(
            "Resumen del Modelo"
        )

        self.resize(
            700,
            450
        )

        self.inicializar_ui()

    def inicializar_ui(self):

        self.setStyleSheet("""
            QWidget{
                background:#222831;
                color:white;
                font-family:Segoe UI;
            }

            QGroupBox{
                border:1px solid #3A4750;
                border-radius:8px;
                margin-top:10px;
                padding-top:12px;
            }

            QTextEdit{
                background:#2D343F;
                border-radius:6px;
                padding:8px;
                font-size:13px;
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

        layout = QVBoxLayout()

        titulo = QLabel(
            "RESUMEN DEL MODELO"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setStyleSheet("""
            background:#1B2A49;
            font-size:20px;
            font-weight:bold;
            padding:10px;
            border-radius:8px;
        """)

        grupo_modelo = QGroupBox(
            "Modelo Generado"
        )

        grupo_layout = QVBoxLayout()

        self.txt_resumen = QTextEdit()

        self.txt_resumen.setReadOnly(
            True
        )

        self.txt_resumen.setText(
            self.generar_resumen()
        )

        grupo_layout.addWidget(
            self.txt_resumen
        )

        grupo_modelo.setLayout(
            grupo_layout
        )

        self.btn_volver = QPushButton(
            "Modificar Modelo Generado"
        )

        self.btn_grafico = QPushButton(
            "Resolver Gráficamente"
        )

        self.btn_simplex = QPushButton(
            "Resolver por Simplex"
        )

        self.btn_salir = QPushButton(
            "Cerrar Aplicación"
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

        self.btn_salir.clicked.connect(
            self.cerrar_programa
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            grupo_modelo
        )

        layout.addWidget(
            self.btn_volver
        )

        layout.addWidget(
            self.btn_grafico
        )

        layout.addWidget(
            self.btn_simplex
        )

        layout.addWidget(
            self.btn_salir
        )

        self.setLayout(
            layout
        )


    def generar_resumen(self):

        texto = ""

        texto += "📌 Nombre del Caso\n"

        texto += (
            f"{self.problema.nombre}\n\n"
        )

        texto += "📌 Variables de Decisión\n"

        for variable in self.problema.variables:

            texto += (
                f"{variable.simbolo} = "
                f"{variable.nombre}\n"
            )

        texto += "\n"

        texto += "📌 Función Objetivo\n"

        texto += (
            self.problema.funcion_objetivo()
        )

        texto += "\n\n"

        texto += "📌 Restricciones\n"

        for indice, restriccion in enumerate(
            self.problema.restricciones,
            start=1
        ):

            texto += (
                f"R{indice}: "
                f"{restriccion.a_texto(self.problema.simbolos())}\n"
            )

        texto += "\n"

        texto += "📌 Condiciones\n"

        texto += (
            ", ".join(
                self.problema.simbolos()
            )
            +
            " >= 0"
        )

        return texto

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