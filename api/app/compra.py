from datetime import date
from typing import List, Optional

from .pago import Pago
from .entrada import Entrada
from .validacionError import ValidacionError
from .usuario import Usuario

#Clase que representa una Compra
class Compra:
    def __init__(self, entradas: List[Entrada], usuario: Usuario, pago: Optional[Pago] = None):
        self.id_compra = None  # ID asignado por la base de datos
        self.fecha = date.today()
        self.entradas = entradas
        self.precio_total = self.calcular_precio_total()
        self.usuario = usuario
        self.pago = pago

    def calcular_precio_total(self) -> float:
        subtotal = sum(entrada.precio for entrada in self.entradas)
        porcentaje_impuestos = 0.15
        impuestos = subtotal * porcentaje_impuestos
        comision_de_plataforma = 1250.50
        return subtotal + impuestos + comision_de_plataforma
    

    def __str__(self):
        return f"fecha={self.fecha},\n forma_pago={self.forma_pago},\n precio_total={self.precio_total},\n usuario={self.usuario.nombre} {self.usuario.apellido},\n entradas= [{' | '.join(str(entrada) for entrada in self.entradas)}]"

