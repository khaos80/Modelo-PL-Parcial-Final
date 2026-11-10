from utils.constantes import SIGNOS_VALIDOS


def validar_nombre(texto: str) -> bool:
    return texto.strip() != ""


def validar_numero(valor) -> bool:
    try:
        float(valor)
        return True
    except ValueError:
        return False


def validar_no_negativo(valor) -> bool:

    try:
        return float(valor) >= 0
    except ValueError:
        return False


def validar_signo(signo: str) -> bool:

    return signo in SIGNOS_VALIDOS


def validar_tipo_objetivo(tipo: str) -> bool:

    return tipo in [
        "MAX",
        "MIN"
    ]


def validar_cantidad_variables(cantidad: int):

    return cantidad >= 2


def validar_cantidad_restricciones(cantidad: int):

    return cantidad >= 1