from PyQt6.QtWidgets import QMessageBox

from models.variable import Variable
from models.restriccion import Restriccion
from models.problema import Problema

from views.resumen_view import ResumenView

from controllers.grafico_controller import (
    GraficoController
)

from controllers.simplex_controller import (
    SimplexController
)


class CapturaController:

    def __init__(self, vista):

        self.vista = vista

        self.problema = None

        self.resumen_view = None

        self.grafico_controller = None

        self.simplex_controller = None

        self.conectar_eventos()

    # ==========================================
    # EVENTOS
    # ==========================================

    def conectar_eventos(self):

        self.vista.btn_resumen.clicked.connect(
            self.generar_resumen
        )

    # ==========================================
    # RESUMEN
    # ==========================================

    def generar_resumen(self):

        try:

            self.problema = (
                self.construir_problema()
            )

            self.resumen_view = ResumenView(
                self.problema
            )

            self.resumen_view.btn_volver.clicked.connect(
                self.volver_captura
            )

            self.resumen_view.btn_grafico.clicked.connect(
                self.abrir_grafico
            )

            self.resumen_view.btn_simplex.clicked.connect(
                self.abrir_simplex
            )

            self.resumen_view.show()

            self.vista.close()

        except Exception as error:

            QMessageBox.warning(

                self.vista,

                "⚠ Información incompleta",

                str(error)
            )

    # ==========================================
    # CONSTRUIR PROBLEMA
    # ==========================================

    def construir_problema(self):

        nombre = (
            self.vista.txt_nombre.text().strip()
        )

        if not nombre:

            raise ValueError(

                "⚠ Nombre del caso requerido\n\n"

                "Debe ingresar un nombre para identificar el modelo."
            )

        tipo_objetivo = (
            self.vista.cmb_objetivo.currentText()
        )

        variables = (
            self.obtener_variables()
        )

        coeficientes_objetivo = (
            self.obtener_objetivo()
        )

        restricciones = (
            self.obtener_restricciones(
                len(variables)
            )
        )

        return Problema(

            nombre=nombre,

            tipo_objetivo=tipo_objetivo,

            variables=variables,

            coeficientes_objetivo=coeficientes_objetivo,

            restricciones=restricciones
        )

    # ==========================================
    # VARIABLES
    # ==========================================

    def obtener_variables(self):

        variables = []

        for fila in range(
            self.vista.tbl_variables.rowCount()
        ):

            item_simbolo = (
                self.vista.tbl_variables.item(
                    fila,
                    0
                )
            )

            item_nombre = (
                self.vista.tbl_variables.item(
                    fila,
                    1
                )
            )

            if item_simbolo is None:

                raise ValueError(
                    f"Falta el símbolo en la variable {fila + 1}"
                )

            if item_nombre is None:

                raise ValueError(
                    f"Falta el nombre de la variable {fila + 1}"
                )

            nombre_variable = (
                item_nombre.text().strip()
            )

            if not nombre_variable:

                raise ValueError(

                    "⚠ Variable incompleta\n\n"

                    f"La variable {item_simbolo.text()} "

                    "no tiene descripción."
                )

            variables.append(

                Variable(
                    simbolo=item_simbolo.text(),
                    nombre=nombre_variable
                )
            )

        return variables

    # ==========================================
    # OBJETIVO
    # ==========================================

    def obtener_objetivo(self):

        coeficientes = []

        for columna in range(
            self.vista.tbl_objetivo.columnCount()
        ):

            item = (
                self.vista.tbl_objetivo.item(
                    0,
                    columna
                )
            )

            if item is None:

                raise ValueError(

                    "⚠ Función objetivo incompleta\n\n"

                    "Todos los coeficientes de la función objetivo "

                    "deben contener un valor numérico."
                )

            texto = (
                item.text().strip()
            )

            if not texto:

                raise ValueError(

                    "⚠ Función objetivo incompleta\n\n"

                    "Todos los coeficientes de la función objetivo "

                    "deben contener un valor numérico."
                )

            coeficientes.append(
                float(texto)
            )

        return coeficientes

    # ==========================================
    # RESTRICCIONES
    # ==========================================

    def obtener_restricciones(
        self,
        cantidad_variables
    ):

        restricciones = []

        filas = (
            self.vista.tbl_restricciones.rowCount()
        )

        for fila in range(filas):

            coeficientes = []

            for columna in range(
                cantidad_variables
            ):

                item = (
                    self.vista.tbl_restricciones.item(
                        fila,
                        columna
                    )
                )

                if item is None:

                    raise ValueError(

                        "⚠ Restricción incompleta\n\n"

                        f"Falta un coeficiente en la restricción "

                        f"R{fila + 1}."
                    )

                texto = item.text().strip()

                if not texto:

                    raise ValueError(

                        "⚠ Restricción incompleta\n\n"

                        f"Falta un coeficiente en la restricción "

                        f"R{fila + 1}."
                    )

                coeficientes.append(
                    float(texto)
                )

            combo_signo = (
                self.vista.tbl_restricciones.cellWidget(
                    fila,
                    cantidad_variables
                )
            )

            signo = (
                combo_signo.currentText()
            )

            item_limite = (
                self.vista.tbl_restricciones.item(
                    fila,
                    cantidad_variables + 1
                )
            )

            if item_limite is None:

                raise ValueError(

                    "⚠ Restricción incompleta\n\n"

                    f"La restricción R{fila + 1} "

                    "no tiene un valor límite."
                )

            texto_limite = (
                item_limite.text().strip()
            )

            if not texto_limite:

                raise ValueError(

                    "⚠ Restricción incompleta\n\n"

                    f"La restricción R{fila + 1} "

                    "no tiene un valor límite."
                )

            limite = float(
                texto_limite
            )

            restricciones.append(

                Restriccion(
                    nombre=f"R{fila+1}",
                    coeficientes=coeficientes,
                    signo=signo,
                    limite=limite
                )
            )

        return restricciones


    def volver_captura(self):

        self.resumen_view.close()

        self.vista.show()

    # ==========================================
    # MÉTODO GRÁFICO
    # ==========================================

    def abrir_grafico(self):

        self.resumen_view.close()

        self.grafico_controller = (
            GraficoController(
                self.problema,
                self.resumen_view
            )
        )

        self.grafico_controller.mostrar()

    # ==========================================
    # MÉTODO SIMPLEX
    # ==========================================

    def abrir_simplex(self):

        self.resumen_view.close()

        self.simplex_controller = (
            SimplexController(
                self.problema,
                self.resumen_view,
                None
            )
        )

        self.simplex_controller.mostrar()