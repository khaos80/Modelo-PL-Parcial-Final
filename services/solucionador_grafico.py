from itertools import combinations

from models.restriccion import Restriccion

from utils.constantes import (
    OPTIMO,
    INFACTIBLE
)


class SolucionadorGrafico:

    TOLERANCIA = 0.0001

    def __init__(self, problema):

        self.problema = problema

    # ==================================================
    # FUNCIÓN OBJETIVO
    # ==================================================
    def evaluar_objetivo(self, punto):

        valor = 0

        for coeficiente, coordenada in zip(
            self.problema.coeficientes_objetivo,
            punto
        ):

            valor += coeficiente * coordenada

        return round(valor, 4)

    # ==================================================
    # FACTIBILIDAD
    # ==================================================
    def es_factible(self, punto):

        x, y = punto

        if x < -self.TOLERANCIA:
            return False

        if y < -self.TOLERANCIA:
            return False

        for restriccion in self.problema.restricciones:

            valor = sum(

                coef * variable

                for coef, variable in zip(
                    restriccion.coeficientes,
                    punto
                )
            )

            limite = restriccion.limite

            if restriccion.signo == "<=":

                if valor > limite + self.TOLERANCIA:
                    return False

            elif restriccion.signo == ">=":

                if valor < limite - self.TOLERANCIA:
                    return False

            elif restriccion.signo == "=":

                if abs(valor - limite) > self.TOLERANCIA:
                    return False

        return True

    # ==================================================
    # INTERSECCIÓN
    # ==================================================
    def obtener_interseccion(self, r1, r2):

        a1, b1 = r1.coeficientes
        a2, b2 = r2.coeficientes

        c1 = r1.limite
        c2 = r2.limite

        determinante = (a1 * b2 - a2 * b1)

        if abs(determinante) < self.TOLERANCIA:

            return None

        x = (c1 * b2 - c2 * b1) / determinante

        y = (a1 * c2 - a2 * c1) / determinante

        return (
            round(x, 6),
            round(y, 6)
        )

    # ==================================================
    # RESTRICCIONES COMPLETAS
    # ==================================================
    def obtener_restricciones_completas(self):

        restricciones = list(
            self.problema.restricciones
        )

        restricciones.append(

            Restriccion(
                nombre="Eje X",
                coeficientes=[1, 0],
                signo="=",
                limite=0
            )
        )

        restricciones.append(

            Restriccion(
                nombre="Eje Y",
                coeficientes=[0, 1],
                signo="=",
                limite=0
            )
        )

        return restricciones

    # ==================================================
    # VÉRTICES
    # ==================================================
    def obtener_vertices(self):

        vertices = []

        restricciones = (
            self.obtener_restricciones_completas()
        )

        for r1, r2 in combinations(
            restricciones,
            2
        ):

            punto = self.obtener_interseccion(
                r1,
                r2
            )

            if punto is None:
                continue

            if punto not in vertices:
                vertices.append(
                    punto
                )

        return vertices

    # ==================================================
    # EVALUAR RESTRICCIONES
    # ==================================================
    def evaluar_restricciones(
        self,
        punto
    ):

        resultado = []

        for restriccion in self.problema.restricciones:

            valor = sum(

                coef * variable

                for coef, variable in zip(
                    restriccion.coeficientes,
                    punto
                )
            )

            limite = restriccion.limite

            if restriccion.signo == "<=":

                cumple = valor <= limite

            elif restriccion.signo == ">=":

                cumple = valor >= limite

            else:

                cumple = (
                    abs(valor - limite)
                    < self.TOLERANCIA
                )

            resultado.append({

                "restriccion":
                restriccion.a_texto(
                    self.problema.simbolos()
                ),

                "valor":
                round(valor, 4),

                "limite":
                limite,

                "signo":
                restriccion.signo,

                "cumple":
                cumple
            })

        return resultado

    # ==================================================
    # RESOLVER
    # ==================================================
    def resolver(self):

        vertices = self.obtener_vertices()

        vertices_factibles = []

        evaluaciones = []

        for punto in vertices:

            if self.es_factible(punto):

                valor_z = (
                    self.evaluar_objetivo(
                        punto
                    )
                )

                vertices_factibles.append(
                    punto
                )

                evaluaciones.append({

                    "punto": punto,

                    "z": valor_z
                })

        solo_mayor_igual = all(

            r.signo == ">="

            for r in self.problema.restricciones

        )

        if solo_mayor_igual and len(vertices_factibles) <= 1:

            return {

                "estado":
                "NO_ACOTADO",

                "vertices":
                vertices,

                "vertices_factibles":
                vertices_factibles,

                "evaluaciones":
                [],

                "punto_optimo":
                None,

                "valor_optimo":
                None
            }

        if not vertices_factibles:

            return {

                "estado": INFACTIBLE,

                "vertices": [],

                "vertices_factibles": [],

                "evaluaciones": [],

                "punto_optimo": None,

                "valor_optimo": None
            }

        mejor_punto = None
        mejor_valor = None

        for evaluacion in evaluaciones:

            punto = evaluacion["punto"]

            valor = evaluacion["z"]

            if mejor_punto is None:

                mejor_punto = punto

                mejor_valor = valor

                continue

            if self.problema.tipo_objetivo == "MAX":

                if valor > mejor_valor:

                    mejor_valor = valor

                    mejor_punto = punto

            else:

                if valor < mejor_valor:

                    mejor_valor = valor

                    mejor_punto = punto

        variables_optimas = {}

        for indice, variable in enumerate(
            self.problema.variables
        ):

            variables_optimas[
                variable.simbolo
            ] = mejor_punto[indice]

        estado_restricciones = (

            self.evaluar_restricciones(
                mejor_punto
            )

        )

        return {

            "estado":
            OPTIMO,

            "modelo":
            self.problema.modelo_completo(),

            "restricciones":

            [
                r.a_texto(
                    self.problema.simbolos()
                )

                for r in self.problema.restricciones
            ],

            "vertices":
            vertices,

            "vertices_factibles":
            vertices_factibles,

            "evaluaciones":
            evaluaciones,

            "punto_optimo":
            mejor_punto,

            "valor_optimo":
            mejor_valor,

            "variables_optimas":
            variables_optimas,

            "estado_restricciones":
            estado_restricciones
        }