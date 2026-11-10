from dataclasses import dataclass


@dataclass
class Variable:

    simbolo: str

    nombre: str

    unidad: str = ""

    def descripcion(self):

        return f"{self.simbolo} = {self.nombre}"