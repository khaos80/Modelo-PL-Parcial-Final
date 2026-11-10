import sys

from PyQt6.QtWidgets import QApplication

from views.inicio_view import InicioView
from views.instrucciones_view import InstruccionesView
from views.captura_view import CapturaView

from controllers.captura_controller import (
    CapturaController
)


class Aplicacion:

    def __init__(self):

        # ==========================
        # VENTANAS
        # ==========================

        self.inicio_view = InicioView()

        self.instrucciones_view = None

        self.captura_view = None

        # ==========================
        # CONTROLADORES
        # ==========================

        self.captura_controller = None

        # ==========================
        # EVENTOS
        # ==========================

        self.conectar_eventos()

    # ==================================
    # EVENTOS
    # ==================================

    def conectar_eventos(self):

        self.inicio_view.btn_crear.clicked.connect(
            self.abrir_captura
        )

        self.inicio_view.btn_instrucciones.clicked.connect(
            self.abrir_instrucciones
        )

        self.inicio_view.btn_salir.clicked.connect(
            self.salir
        )

    # ==================================
    # MOSTRAR INICIO
    # ==================================

    def mostrar_inicio(self):

        self.inicio_view.show()

    # ==================================
    # ABRIR CAPTURA
    # ==================================

    def abrir_captura(self):

        self.inicio_view.close()

        self.captura_view = CapturaView()

        self.captura_controller = (
            CapturaController(
                self.captura_view
            )
        )

        self.captura_view.show()

    # ==================================
    # ABRIR INSTRUCCIONES
    # ==================================

    def abrir_instrucciones(self):

        self.inicio_view.close()

        self.instrucciones_view = (
            InstruccionesView()
        )

        self.instrucciones_view.btn_volver.clicked.connect(
            self.volver_inicio
        )

        self.instrucciones_view.show()

    # ==================================
    # VOLVER A INICIO
    # ==================================

    def volver_inicio(self):

        if self.instrucciones_view:

            self.instrucciones_view.close()

        self.inicio_view.show()

    # ==================================
    # SALIR
    # ==================================

    def salir(self):

        self.inicio_view.close()

    # ==================================
    # EJECUTAR
    # ==================================

    def ejecutar(self):

        self.mostrar_inicio()


def main():

    app = QApplication(
        sys.argv
    )

    programa = Aplicacion()

    programa.ejecutar()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()