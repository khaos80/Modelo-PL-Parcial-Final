from dataclasses import dataclass


@dataclass
class Restriccion:

    nombre: str

    coeficientes: list

    signo: str

    limite: float

    def es_valida(self):

        return self.signo in [
            "<=",
            ">=",
            "="
        ]

    def a_texto(
        self,
        simbolos: list
    ):

        partes = []

        for indice, (coef, simbolo) in enumerate(
            zip(
                self.coeficientes,
                simbolos
            )
        ):

            # Omitir coeficientes 0

            if abs(coef) < 0.000001:
                continue

            coef_abs = abs(coef)

            # Mostrar enteros sin .0

            if float(coef).is_integer():

                valor = str(
                    int(abs(coef))
                )

            else:

                valor = str(
                    round(
                        abs(coef),
                        4
                    )
                )

            termino = (
                f"{valor}{simbolo}"
            )

            if len(partes) == 0:

                if coef < 0:

                    partes.append(
                        f"-{termino}"
                    )

                else:

                    partes.append(
                        termino
                    )

            else:

                if coef < 0:

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

        if float(self.limite).is_integer():

            limite = str(
                int(self.limite)
            )

        else:

            limite = str(
                round(
                    self.limite,
                    4
                )
            )

        return (
            f"{expresion} "
            f"{self.signo} "
            f"{limite}"
        )
