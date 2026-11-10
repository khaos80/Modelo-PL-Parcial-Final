from models.problema import Problema


class GeneradorModelo:

    @staticmethod
    def generar(problema: Problema) -> str:

        return problema.modelo_completo()