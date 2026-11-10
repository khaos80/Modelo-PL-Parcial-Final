from dataclasses import dataclass

from models.variable import Variable
from models.restriccion import Restriccion


@dataclass
class Problema:

    nombre: str

    tipo_objetivo: str

    variables: list[Variable]

    coeficientes_objetivo: list

    restricciones: list[Restriccion]

    unidad_medida: str = ""

    def simbolos(self):

        return [
            variable.simbolo
            for variable in self.variables
        ]

    def funcion_objetivo(self):

            partes = []

            for coeficiente, variable in zip(
                self.coeficientes_objetivo,
                self.variables
            ):

                if abs(coeficiente) < 0.000001:
                    continue

                valor_abs = abs(coeficiente)

                if float(valor_abs).is_integer():

                    coef = str(
                        int(valor_abs)
                    )

                else:

                    coef = str(
                        round(
                            valor_abs,
                            4
                        )
                    )

                termino = (
                    f"{coef}{variable.simbolo}"
                )

                if len(partes) == 0:

                    if coeficiente < 0:

                        partes.append(
                            f"-{termino}"
                        )

                    else:

                        partes.append(
                            termino
                        )

                else:

                    if coeficiente < 0:

                        partes.append(
                            f"- {termino}"
                        )

                    else:

                        partes.append(
                            f"+ {termino}"
                        )

            if not partes:

                expresion = "0"

            else:

                expresion = " ".join(
                    partes
                )

            return (
                f"{self.tipo_objetivo} Z = "
                f"{expresion}"
            )


    def modelo_completo(self):

        texto = []

        texto.append(
            self.funcion_objetivo()
        )

        texto.append("")
        texto.append("Sujeto a:")

        for restriccion in self.restricciones:

            texto.append(
                restriccion.a_texto(
                    self.simbolos()
                )
            )

        texto.append("")

        texto.append(
            f'{", ".join(self.simbolos())} >= 0'
        )

        return "\n".join(texto)