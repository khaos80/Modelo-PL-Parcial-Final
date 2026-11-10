import numpy as np

from PyQt6.QtWidgets import QMessageBox

from controllers.simplex_controller import (
    SimplexController
)

from services.solucionador_grafico import (
    SolucionadorGrafico
)

from views.grafico_view import (
    GraficoView
)


class GraficoController:

    def __init__(
        self,
        problema,
        resumen_view
    ):

        self.problema = problema

        self.resumen_view = resumen_view

        self.vista = GraficoView()

        self.resultado = None

        self.simplex_controller = None

    # ==========================================
    # MOSTRAR
    # ==========================================

    def mostrar(self):

        try:

            if len(self.problema.variables) != 2:

                QMessageBox.information(

                    self.resumen_view,

                    "⚠ Método gráfico no disponible",

                    "El método gráfico únicamente puede "
                    "trabajar con modelos de 2 variables.\n\n"

                    "Para este modelo utilice el método simplex."
                )

                self.resumen_view.show()

                return

            self.resultado = (

                SolucionadorGrafico(
                    self.problema
                ).resolver()

            )

            estado = self.resultado.get(
                "estado",
                "DESCONOCIDO"
            )

            if estado != "OPTIMO":

                if estado == "INFACTIBLE":

                    QMessageBox.warning(

                        self.resumen_view,

                        "⚠ Modelo infactible",

                        "No existe ninguna solución que "

                        "cumpla simultáneamente todas las restricciones."
                    )

                elif estado == "NO_ACOTADO":

                    QMessageBox.warning(

                        self.resumen_view,

                        "⚠ Modelo no acotado",

                        "La función objetivo puede crecer "

                        "indefinidamente dentro de la región "

                        "factible.\n\n"

                        "No existe una solución óptima finita."
                    )

                else:

                    QMessageBox.warning(

                        self.resumen_view,

                        "⚠ Resultado no reconocido",

                        f"El modelo terminó con estado: {estado}"
                    )

                self.resumen_view.show()

                return
                
        except Exception as error:

            QMessageBox.critical(

                self.resumen_view,

                "⚠ Error inesperado",

                "Ocurrió un problema al ejecutar "
                "el método gráfico.\n\n"

                f"Detalle:\n{error}"
            )

            self.resumen_view.show()

            return

        # ==========================
        # DASHBOARD
        # ==========================

        self.cargar_dashboard()

        self.vista.btn_volver_resumen.clicked.connect(
            self.volver_resumen
        )

        self.vista.btn_simplex.clicked.connect(
            self.abrir_simplex
        )

        self.vista.show()

    # ==========================================
    # DASHBOARD
    # ==========================================

    def cargar_dashboard(self):

        self.vista.cargar_resultado(

            self.resultado[
                "variables_optimas"
            ],

            self.resultado[
                "valor_optimo"
            ]
        )

        self.vista.cargar_vertices(

            self.resultado[
                "evaluaciones"
            ],

            self.problema.tipo_objetivo
        )

        self.vista.cargar_restricciones(

            self.resultado[
                "estado_restricciones"
            ]
        )

        self.dibujar_grafica()

    # ==========================================
    # GRÁFICA
    # ==========================================

    def dibujar_grafica(self):

        self.vista.limpiar_grafica()

        ax = self.vista.ax

        # ==================================
        # TEMA OSCURO
        # ==================================

        ax.set_facecolor("#121212")

        self.vista.figure.patch.set_facecolor(
            "#121212"
        )

        ax.tick_params(
            colors="white"
        )

        ax.xaxis.label.set_color("white")

        ax.yaxis.label.set_color("white")

        ax.title.set_color("white")

        for spine in ax.spines.values():

            spine.set_color(
                "white"
            )

        restricciones = (
            self.problema.restricciones
        )

        vertices = (
            self.resultado[
                "vertices_factibles"
            ]
        )

        max_x = 10
        max_y = 10

        for restriccion in restricciones:

            max_x = max(
                max_x,
                restriccion.limite
            )

            max_y = max(
                max_y,
                restriccion.limite
            )

        x = np.linspace(
            0,
            max_x * 1.2,
            500
        )

        colores = [
            "#1976D2",
            "#F57C00",
            "#388E3C",
            "#7B1FA2",
            "#C2185B"
        ]

        # ==================================
        # RESTRICCIONES
        # ==================================

        for indice, restriccion in enumerate(
            restricciones
        ):

            if len(
                restriccion.coeficientes
            ) != 2:

                continue

            a, b = (
                restriccion.coeficientes
            )

            c = (
                restriccion.limite
            )

            if b == 0:

                ax.axvline(

                    x=c / a,

                    color=colores[
                        indice % len(colores)
                    ],

                    linewidth=2,

                    label=restriccion.a_texto(
                        self.problema.simbolos()
                    )
                )

                continue

            y = (
                c - a * x
            ) / b

            ax.plot(

                x,

                y,

                linewidth=2,

                color=colores[
                    indice % len(colores)
                ],

                label=restriccion.a_texto(
                    self.problema.simbolos()
                )
            )

        # ==================================
        # REGION FACTIBLE
        # ==================================

        if len(vertices) >= 3:

            centro_x = sum(
                p[0]
                for p in vertices
            ) / len(vertices)

            centro_y = sum(
                p[1]
                for p in vertices
            ) / len(vertices)

            vertices_ordenados = sorted(

                vertices,

                key=lambda p:
                np.arctan2(
                    p[1] - centro_y,
                    p[0] - centro_x
                )
            )

            xs = [
                p[0]
                for p in vertices_ordenados
            ]

            ys = [
                p[1]
                for p in vertices_ordenados
            ]

            ax.fill(

                xs,

                ys,

                color="#42A5F5",

                alpha=0.20,

                hatch="///",

                edgecolor="#90CAF9",

                linewidth=1.5,

                label="Región Factible"
            )

        # ==================================
        # OPTIMOS
        # ==================================

        if self.problema.tipo_objetivo == "MAX":

            mejor_z = max(

                e["z"]

                for e in self.resultado[
                    "evaluaciones"
                ]
            )

        else:

            mejor_z = min(

                e["z"]

                for e in self.resultado[
                    "evaluaciones"
                ]
            )

        puntos_optimos = []

        for evaluacion in self.resultado[
            "evaluaciones"
        ]:

            if abs(
                evaluacion["z"]
                -
                mejor_z
            ) < 0.000001:

                puntos_optimos.append(
                    evaluacion["punto"]
                )

        # ==================================
        # VERTICES
        # ==================================

        for punto in vertices:

            es_optimo = (
                punto in puntos_optimos
            )

            valor_z = None

            for evaluacion in self.resultado[
                "evaluaciones"
            ]:

                if evaluacion["punto"] == punto:

                    valor_z = (
                        evaluacion["z"]
                    )

                    break

            ax.scatter(

                punto[0],

                punto[1],

                color=
                "#FF8A80"
                if es_optimo
                else "white",

                edgecolors=
                "#FF0000"
                if es_optimo
                else "#90CAF9",

                linewidths=
                2
                if es_optimo
                else 1,

                s=
                110
                if es_optimo
                else 60,

                zorder=5
            )

            texto = (

                f"({self.vista.formatear_numero(punto[0])}, "
                f"{self.vista.formatear_numero(punto[1])})\n"

                f"Z = {self.vista.formatear_numero(valor_z)}"
            )

            ax.annotate(

                texto,

                (
                    punto[0],
                    punto[1]
                ),

                xytext=(12, 12),

                textcoords="offset points",

                fontsize=8,

                color="white",

                bbox=dict(

                    boxstyle="round,pad=0.35",

                    fc=
                    "#6A0000"
                    if es_optimo
                    else "#1E1E1E",

                    ec=
                    "#FF5252"
                    if es_optimo
                    else "#90CAF9",

                    alpha=0.95
                )
            )

        # ==================================
        # RESALTAR TODOS LOS OPTIMOS
        # ==================================

        for punto in puntos_optimos:

            ax.scatter(

                punto[0],

                punto[1],

                color="#FF5252",

                edgecolors="#FF0000",

                linewidths=3,

                s=220,

                zorder=10
            )

        # ==================================
        # FUNCION OBJETIVO
        # ==================================

        try:

            z = self.resultado[
                "valor_optimo"
            ]

            c1 = (
                self.problema
                .coeficientes_objetivo[0]
            )

            c2 = (
                self.problema
                .coeficientes_objetivo[1]
            )

            if c2 != 0:

                y_obj = (
                    z - c1 * x
                ) / c2

                ax.plot(

                    x,

                    y_obj,

                    "--",

                    color="#00E676",

                    linewidth=2,

                    label=f"Z={self.vista.formatear_numero(z)}"
                )

        except Exception:

            pass

        # ==================================
        # ESTILO
        # ==================================

        ax.set_xlim(left=0)

        ax.set_ylim(bottom=0)

        ax.grid(

            True,

            linestyle="--",

            linewidth=0.5,

            color="white",

            alpha=0.25
        )

        legend = ax.legend()

        legend.get_frame().set_facecolor(
            "#1E1E1E"
        )

        legend.get_frame().set_edgecolor(
            "#90CAF9"
        )

        for texto in legend.get_texts():

            texto.set_color(
                "white"
            )

        self.vista.canvas.draw()

    # ==========================================
    # SIMPLEX
    # ==========================================

    def abrir_simplex(self):

        self.vista.close()

        self.simplex_controller = (

            SimplexController(
                self.problema,
                self.resumen_view,
                self
            )

        )

        self.simplex_controller.mostrar()

    # ==========================================
    # VOLVER A RESUMEN
    # ==========================================

    def volver_resumen(self):

        self.vista.close()

        self.resumen_view.show()