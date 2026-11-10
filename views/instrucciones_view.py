from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QFrame
)

from PyQt6.QtCore import Qt


class InstruccionesView(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Instrucciones"
        )

        self.resize(
            1000,
            750
        )

        self.inicializar_ui()

    def inicializar_ui(self):

        self.setStyleSheet("""
            QWidget{
                background-color:#222831;
                color:white;
                font-family:Segoe UI;
            }

            QTextEdit{
                background-color:#2D343F;
                color:white;
                border:1px solid #3A4750;
                border-radius:8px;
                padding:10px;
                font-size:13px;
            }

            QPushButton{
                background-color:#1B2A49;
                color:white;
                border:none;
                border-radius:8px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background-color:#28457D;
            }
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            30,
            20,
            30,
            20
        )

        # ==================================
        # CABECERA
        # ==================================

        titulo = QLabel(
            "INSTRUCCIONES DEL SISTEMA"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setStyleSheet("""
            background:#1B2A49;
            padding:15px;
            border-radius:10px;
            font-size:22px;
            font-weight:bold;
        """)

        subtitulo = QLabel(
            "Sistema para Formulación y Resolución de Modelos de Programación Lineal"
        )

        subtitulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitulo.setStyleSheet("""
            font-size:15px;
            color:#D6D6D6;
        """)

        separador = QFrame()

        separador.setFrameShape(
            QFrame.Shape.HLine
        )

        # ==================================
        # CONTENIDO
        # ==================================

        self.txt_instrucciones = QTextEdit()

        self.txt_instrucciones.setReadOnly(
            True
        )

        self.txt_instrucciones.setText(
            """
📌 OBJETIVO DEL SISTEMA

Este aplicativo permite construir y resolver modelos
de Programación Lineal mediante Método Gráfico y
Método Simplex.

══════════════════════════════════════

✅ PASO 1

Pulse "Crear Modelo".

══════════════════════════════════════

✅ PASO 2

Ingrese:

• Nombre del problema.
• Tipo de optimización (MAX o MIN).
• Variables de decisión.

══════════════════════════════════════

✅ PASO 3

Registre los coeficientes de la función objetivo.

Ejemplo:

Max Z = 4X + 6Y

══════════════════════════════════════

✅ PASO 4

Ingrese las restricciones.

Ejemplo:

X + Y ≤ 8

2X + Y ≤ 10

══════════════════════════════════════

✅ PASO 5

Genere el resumen del modelo.

Verifique:

• Variables.
• Función objetivo.
• Restricciones.
• Condiciones de no negatividad.

══════════════════════════════════════

✅ PASO 6

Seleccione:

• Resolver Gráficamente
o
• Resolver mediante Simplex

══════════════════════════════════════

✅ MÉTODO GRÁFICO

Permite visualizar:

• Restricciones.
• Región factible.
• Vértices factibles.
• Punto óptimo.
• Valor óptimo.

══════════════════════════════════════

✅ MÉTODO SIMPLEX

Permite visualizar:

• Tabla inicial.
• Variables entrantes.
• Variables salientes.
• Elementos pivote.
• Iteraciones.
• Solución óptima.

══════════════════════════════════════

⚠ RECOMENDACIONES

• Complete todos los campos.
• Utilice únicamente valores numéricos.
• No deje restricciones incompletas.
• Verifique los signos:
      <=
      >=
      =

══════════════════════════════════════

🎓 Proyecto académico de
Programación Lineal
Ingeniería de Sistemas
            """
        )

        # ==================================
        # BOTÓN VOLVER
        # ==================================

        self.btn_volver = QPushButton(
            "Volver al Inicio"
        )

        # ==================================
        # LAYOUT
        # ==================================

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            subtitulo
        )

        layout.addWidget(
            separador
        )

        layout.addWidget(
            self.txt_instrucciones
        )

        layout.addWidget(
            self.btn_volver
        )

        self.setLayout(
            layout
        )