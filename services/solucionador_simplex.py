from copy import deepcopy


class SolucionadorSimplex:

    TOLERANCIA = 0.0001

    BIG_M = 1000000

    def __init__(self, problema):

        self.problema = problema

        self.tablas = []

        self.variables = []

        self.variables_base = []

        self.variables_holgura = []

        self.variables_exceso = []

        self.variables_artificiales = []

    # ==================================================
    # CONVERTIR A FORMA ESTÁNDAR
    # ==================================================

    def convertir_a_estandar(self):

        restricciones = []

        self.variables_holgura = []
        self.variables_exceso = []
        self.variables_artificiales = []

        for indice, restriccion in enumerate(
            self.problema.restricciones
        ):

            fila = list(
                restriccion.coeficientes
            )

            extras = []

            # <=
            if restriccion.signo == "<=":

                nombre = f"S{indice + 1}"

                self.variables_holgura.append(
                    nombre
                )

                extras.append(
                    (nombre, 1)
                )

            # >=
            elif restriccion.signo == ">=":

                nombre_exceso = f"E{indice + 1}"

                nombre_artificial = f"A{indice + 1}"

                self.variables_exceso.append(
                    nombre_exceso
                )

                self.variables_artificiales.append(
                    nombre_artificial
                )

                extras.append(
                    (nombre_exceso, -1)
                )

                extras.append(
                    (nombre_artificial, 1)
                )

            # =
            elif restriccion.signo == "=":

                nombre_artificial = f"A{indice + 1}"

                self.variables_artificiales.append(
                    nombre_artificial
                )

                extras.append(
                    (nombre_artificial, 1)
                )

            restricciones.append({

                "coeficientes": fila,

                "extras": extras,

                "rhs": restriccion.limite
            })

        variables_extra = (

            self.variables_holgura
            +
            self.variables_exceso
            +
            self.variables_artificiales

        )

        return (
            restricciones,
            variables_extra
        )

    # ==================================================
    # TABLA INICIAL
    # ==================================================

    def crear_tabla_inicial(self):

        restricciones, variables_extra = (
            self.convertir_a_estandar()
        )

        # ==========================
        # VARIABLES TOTALES
        # ==========================

        nombres_variables = [

            variable.simbolo

            for variable in self.problema.variables

        ] + variables_extra

        self.variables = nombres_variables

        # ==========================
        # BASE INICIAL
        # ==========================

        self.variables_base = []

        for indice, restriccion in enumerate(
            self.problema.restricciones
        ):

            if restriccion.signo == "<=":

                self.variables_base.append(
                    f"S{indice + 1}"
                )

            else:

                self.variables_base.append(
                    f"A{indice + 1}"
                )

        # ==========================
        # CONSTRUIR TABLA
        # ==========================

        tabla = []

        for restriccion in restricciones:

            fila = []

            fila.extend(
                restriccion["coeficientes"]
            )

            for variable in variables_extra:

                valor = 0

                for nombre, coef in restriccion["extras"]:

                    if variable == nombre:

                        valor = coef

                        break

                fila.append(valor)

            fila.append(
                restriccion["rhs"]
            )

            tabla.append(
                fila
            )

        # ==========================
        # FILA Z
        # ==========================

        fila_z = []

        if self.problema.tipo_objetivo == "MAX":

            for coef in self.problema.coeficientes_objetivo:

                fila_z.append(
                    -coef
                )

        else:

            for coef in self.problema.coeficientes_objetivo:

                fila_z.append(
                    coef
                )

        for variable in variables_extra:

            if variable.startswith("A"):

                if self.problema.tipo_objetivo == "MAX":

                    fila_z.append(
                        -self.BIG_M
                    )

                else:

                    fila_z.append(
                        self.BIG_M
                    )

            else:

                fila_z.append(0)

        fila_z.append(0)

        for indice_fila, variable_base in enumerate(
            self.variables_base
        ):

            if variable_base.startswith("A"):

                fila_base = tabla[
                    indice_fila
                ]

                multiplicador = self.BIG_M

                if self.problema.tipo_objetivo == "MIN":

                    multiplicador *= -1

                for columna in range(
                    len(fila_z)
                ):

                    fila_z[columna] -= (

                        multiplicador
                        *
                        fila_base[columna]

                    )

        tabla.append(
            fila_z
        )

        return tabla

    # ==================================================
    # ¿ES ÓPTIMA?
    # ==================================================

    def es_optima(
        self,
        tabla
    ):

        fila_z = tabla[-1]

        if self.problema.tipo_objetivo == "MAX":

            for valor in fila_z[:-1]:

                if valor < -self.TOLERANCIA:

                    return False

        else:

            for valor in fila_z[:-1]:

                if valor > self.TOLERANCIA:

                    return False

        return True

    # ==================================================
    # COLUMNA PIVOTE
    # ==================================================

    def obtener_columna_pivote(
        self,
        tabla
    ):

        fila_z = tabla[-1][:-1]

        mejor_indice = None

        if self.problema.tipo_objetivo == "MAX":

            mejor_valor = 0

            for indice, valor in enumerate(
                fila_z
            ):

                variable = self.variables[indice]

                if variable.startswith("A"):

                    continue

                if valor < mejor_valor:

                    mejor_valor = valor

                    mejor_indice = indice

        else:

            mejor_valor = 0

            for indice, valor in enumerate(
                fila_z
            ):

                variable = self.variables[indice]

                if variable.startswith("A"):

                    continue

                if valor > mejor_valor:

                    mejor_valor = valor

                    mejor_indice = indice

        return mejor_indice

    # ==================================================
    # FILA PIVOTE
    # ==================================================

    def obtener_fila_pivote(
        self,
        tabla,
        columna_pivote
    ):
        
        candidatos = []

        for i in range(
            len(tabla) - 1
        ):

            divisor = tabla[i][
                columna_pivote
            ]

            if divisor <= 0:

                continue

            razon = (

                tabla[i][-1]
                /
                divisor

            )

            candidatos.append(
                (
                    razon,
                    i
                )
            )

        if not candidatos:

            return None

        candidatos.sort()

        return candidatos[0][1]

    # ==================================================
    # PIVOTEO
    # ==================================================

    def pivotear(
        self,
        tabla,
        fila_pivote,
        columna_pivote
    ):

        nueva_tabla = deepcopy(
            tabla
        )

        pivote = nueva_tabla[
            fila_pivote
        ][columna_pivote]

        # Normalizar fila pivote

        nueva_tabla[
            fila_pivote
        ] = [

            valor / pivote

            for valor in
            nueva_tabla[
                fila_pivote
            ]

        ]

        # Hacer ceros

        for fila in range(
            len(nueva_tabla)
        ):

            if fila == fila_pivote:

                continue

            factor = nueva_tabla[
                fila
            ][columna_pivote]

            nueva_tabla[fila] = [

                actual
                -
                factor * pivote_valor

                for actual,
                pivote_valor

                in zip(
                    nueva_tabla[fila],
                    nueva_tabla[
                        fila_pivote
                    ]
                )
            ]

        return nueva_tabla

    # ==================================================
    # GUARDAR ITERACIÓN
    # ==================================================

    def guardar_iteracion(
        self,
        numero,
        tabla,
        columna_pivote=None,
        fila_pivote=None,
        variable_entrante=None,
        variable_saliente=None,
        pivote=None
    ):

        self.tablas.append({

            "numero":
            numero,

            "tabla":
            deepcopy(tabla),

            "variables":
            self.variables.copy(),

            "base":
            self.variables_base.copy(),

            "columna_pivote":
            columna_pivote,

            "fila_pivote":
            fila_pivote,

            "variable_entrante":
            variable_entrante,

            "variable_saliente":
            variable_saliente,

            "pivote":
            pivote
        })

    # ==================================================
    # OBTENER SOLUCIÓN
    # ==================================================

    def obtener_solucion(
        self,
        tabla
    ):

        solucion = {}

        for variable in self.variables:

            solucion[
                variable
            ] = 0

        for indice, variable_base in enumerate(
            self.variables_base
        ):

            solucion[
                variable_base
            ] = tabla[
                indice
            ][-1]

        variables_decision = {}

        for variable in (
            self.problema.variables
        ):

            variables_decision[
                variable.simbolo
            ] = solucion.get(
                variable.simbolo,
                0
            )

        valor_optimo = tabla[-1][-1]

        return (
            variables_decision,
            valor_optimo
        )

    # ==================================================
    # RESOLVER
    # ==================================================

    def resolver(self):

        tabla = (
            self.crear_tabla_inicial()
        )

        numero_iteracion = 0

        self.guardar_iteracion(

            numero_iteracion,

            tabla
        )

        while not self.es_optima(
            tabla
        ):

            numero_iteracion += 1

            columna_pivote = (

                self.obtener_columna_pivote(
                    tabla
                )
            )

            if columna_pivote is None:

                break

            fila_pivote = (

                self.obtener_fila_pivote(
                    tabla,
                    columna_pivote
                )
            )

            if fila_pivote is None:

                return {

                    "estado":
                    "NO_ACOTADO",

                    "iteraciones":
                    self.tablas
                }

            variable_entrante = (

                self.variables[
                    columna_pivote
                ]
            )

            variable_saliente = (

                self.variables_base[
                    fila_pivote
                ]
            )

            pivote = tabla[
                fila_pivote
            ][
                columna_pivote
            ]

            self.variables_base[
                fila_pivote
            ] = variable_entrante

            tabla = self.pivotear(

                tabla,

                fila_pivote,

                columna_pivote
            )

            self.guardar_iteracion(

                numero_iteracion,

                tabla,

                columna_pivote,

                fila_pivote,

                variable_entrante,

                variable_saliente,

                pivote
            )

        for indice, variable_base in enumerate(
            self.variables_base
        ):

            if variable_base.startswith("A"):

                valor = tabla[indice][-1]

                if abs(valor) > self.TOLERANCIA:

                    return {

                        "estado":
                        "INFACTIBLE",

                        "iteraciones":
                        self.tablas
                    }        

        solucion, valor_optimo = (

            self.obtener_solucion(
                tabla
            )
        )

        return {

            "estado":
            "OPTIMO",

            "iteraciones":
            self.tablas,

            "solucion":
            solucion,

            "valor_optimo":
            valor_optimo
        }