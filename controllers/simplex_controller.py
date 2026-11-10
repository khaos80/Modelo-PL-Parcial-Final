from views.simplex_view import (
    SimplexView
)

from services.solucionador_simplex import (
    SolucionadorSimplex
)

from PyQt6.QtWidgets import QMessageBox

class SimplexController:

    def __init__(
        self,
        problema,
        resumen_view,
        grafico_controller=None
    ):

        self.problema = problema

        self.resumen_view = resumen_view

        self.grafico_controller = grafico_controller

        self.vista = SimplexView()

        self.resultado = None

    # ==================================
    # MOSTRAR
    # ==================================

    def mostrar(self):

        try:

            self.resultado = (

                SolucionadorSimplex(
                    self.problema
                ).resolver()

            )

            estado = self.resultado.get(
                "estado",
                "DESCONOCIDO"
            )

            if estado == "INFACTIBLE":

                QMessageBox.warning(

                    self.resumen_view,

                    "⚠ Modelo infactible",

                    "No existe ninguna solución que "
                    "cumpla simultáneamente todas las restricciones."
                )

                self.resumen_view.show()

                return

            elif estado == "NO_ACOTADO":

                QMessageBox.warning(

                    self.resumen_view,

                    "⚠ Modelo no acotado",

                    "La función objetivo puede crecer "
                    "indefinidamente dentro de la región "
                    "factible.\n\n"

                    "No existe una solución óptima finita."
                )

                self.resumen_view.show()

                return

            self.vista.cargar_resultado(
                self.resultado
            )

            self.vista.show()

            self.vista.btn_anterior.clicked.connect(
                self.anterior
            )

            self.vista.btn_siguiente.clicked.connect(
                self.siguiente
            )

            self.vista.btn_resumen.clicked.connect(
                self.volver_resumen
            )

            self.vista.btn_grafico.clicked.connect(
                self.volver_grafico
            )

            self.vista.show()

        except Exception as error:

            QMessageBox.critical(

                self.resumen_view,

                "⚠ Error inesperado",

                "Ocurrió un problema al ejecutar "
                "el método simplex.\n\n"

                f"Detalle:\n{error}"
            )

    # ==================================
    # ITERACIÓN ANTERIOR
    # ==================================

    def anterior(self):

        if (
            self.vista.iteracion_actual > 0
        ):

            self.vista.iteracion_actual -= 1

            self.vista.mostrar_iteracion()

    # ==================================
    # ITERACIÓN SIGUIENTE
    # ==================================

    def siguiente(self):

        total = len(
            self.resultado[
                "iteraciones"
            ]
        )

        if (
            self.vista.iteracion_actual
            <
            total - 1
        ):

            self.vista.iteracion_actual += 1

            self.vista.mostrar_iteracion()

    # ==================================
    # VOLVER AL RESUMEN
    # ==================================

    def volver_resumen(self):

        self.vista.close()

        self.resumen_view.show()

    # ==================================
    # VOLVER AL MÉTODO GRÁFICO
    # ==================================

    def volver_grafico(self):

        self.vista.close()

        if self.grafico_controller:

            self.grafico_controller.vista.show()

        else:

            from controllers.grafico_controller import (
                GraficoController
            )

            self.grafico_controller = (
                GraficoController(
                    self.problema,
                    self.resumen_view
                )
            )

            self.grafico_controller.mostrar()