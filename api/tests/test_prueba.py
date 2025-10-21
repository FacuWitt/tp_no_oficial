import pytest
from datetime import date, timedelta

# TODO -> Commitear luego de los tests, cuando ya hayan implementaciones
from fastapi.testclient import TestClient
from app.api import app
from app.usuario import Usuario
from app.entrada import Entrada
from app.validacionError import ValidacionError
from app.compra import Compra
from app.servicioCompraEntradas import ServicioCompraEntradas

service = ServicioCompraEntradas()
client = TestClient(app)
# ------------------------------------------------------------------------


def test_read_root():
    resp = client.get("/")
    assert resp.json() == {"message": "Hola, somos el grupo 1 de la materia ISW!"}

# Test para la compra de entradas (PASA)
def test_post_validar_compra_entradas_con_tarjeta():
    body_post_json = {
                    "forma_pago": "tarjeta",
                    "entradas": [
                        {
                            "edad_visitante": 30,
                            "tipo_pase": "VIP",
                            "precio": 2000.0
                        },
                        {
                            "edad_visitante": 25,
                            "tipo_pase": "Regular",
                            "precio": 1000.0
                        }
                    ],
                    "fecha_visita": "2025-12-15",
                    "id_usuario": 1
                }

    resp = client.post("/validar-compra-entradas", json=body_post_json)
    resp_json = resp.json()
    assert resp_json["status_code"] == 200
    assert resp_json["message"] == "Compra validada con éxito"
    assert "detalle_compra" in resp_json
    assert resp_json["detalle_compra"]["fecha_compra"] == str(date.today())
    assert resp_json["detalle_compra"]["precio_total"] == 4700.5 # 100 + 70 + (170 * 0.15) + 1250.5
    assert resp_json["detalle_compra"]["usuario"]["id"] == 1
    assert resp_json["detalle_compra"]["pago"]["forma_pago"] == "tarjeta"
    assert resp_json["detalle_compra"]["pago"]["estado"] == "PAGO_PENDIENTE_POR_MERCADO_PAGO"
    assert resp_json["detalle_compra"]["entradas"][0]["edad_visitante"] == 30
    assert resp_json["detalle_compra"]["entradas"][0]["tipo_pase"] == "VIP"
    assert resp_json["detalle_compra"]["entradas"][0]["precio"] == 2000.0
    assert resp_json["detalle_compra"]["entradas"][0]["fecha_visita"] == "2025-12-15"
    assert resp_json["detalle_compra"]["entradas"][1]["edad_visitante"] == 25
    assert resp_json["detalle_compra"]["entradas"][1]["tipo_pase"] == "Regular"
    assert resp_json["detalle_compra"]["entradas"][1]["precio"] == 1000.0
    assert resp_json["detalle_compra"]["entradas"][1]["fecha_visita"] == "2025-12-15"
    assert len(resp_json["detalle_compra"]["entradas"]) == 2
    assert resp_json["envio_de_mail"] == "PENDIENTE"
def test_post_validar_compra_entradas_con_efectivo():
    body_post_json = {
                    "forma_pago": "efectivo",
                    "entradas": [
                        {
                            "edad_visitante": 30,
                            "tipo_pase": "VIP",
                            "precio": 2000.0
                        },
                        {
                            "edad_visitante": 25,
                            "tipo_pase": "Regular",
                            "precio": 1000.0
                        }
                    ],
                    "fecha_visita": "2025-12-15",
                    "id_usuario": 1
                }

    resp = client.post("/validar-compra-entradas", json=body_post_json)
    resp_json = resp.json()
    assert resp_json["status_code"] == 200
    assert resp_json["message"] == "Compra validada con éxito"
    assert "detalle_compra" in resp_json
    assert resp_json["detalle_compra"]["fecha_compra"] == str(date.today())
    assert resp_json["detalle_compra"]["precio_total"] == 4700.5 # 100 + 70 + (170 * 0.15) + 1250.5
    assert resp_json["detalle_compra"]["usuario"]["id"] == 1
    assert resp_json["detalle_compra"]["pago"]["forma_pago"] == "efectivo"
    assert resp_json["detalle_compra"]["pago"]["estado"] == "PAGO_A_REALIZAR_EN_CAJA"
    assert resp_json["detalle_compra"]["entradas"][0]["edad_visitante"] == 30
    assert resp_json["detalle_compra"]["entradas"][0]["tipo_pase"] == "VIP"
    assert resp_json["detalle_compra"]["entradas"][0]["precio"] == 2000.0
    assert resp_json["detalle_compra"]["entradas"][0]["fecha_visita"] == "2025-12-15"
    assert resp_json["detalle_compra"]["entradas"][1]["edad_visitante"] == 25
    assert resp_json["detalle_compra"]["entradas"][1]["tipo_pase"] == "Regular"
    assert resp_json["detalle_compra"]["entradas"][1]["precio"] == 1000.0
    assert resp_json["detalle_compra"]["entradas"][1]["fecha_visita"] == "2025-12-15"
    assert len(resp_json["detalle_compra"]["entradas"]) == 2
    assert resp_json["envio_de_mail"] == "ENVIADO"
def test_post_validar_compra_entradas_falta_dato_forma_pago():
    compra_data_incompleta = {
                    "entradas": [
                        {
                            "edad_visitante": 30,
                            "tipo_pase": "VIP",
                            "precio": 100.0
                        }
                    ],
                    "fecha_visita": "2024-12-15",
                    "id_usuario": 1
                }

    resp = client.post("/validar-compra-entradas", json=compra_data_incompleta)
    resp_json = resp.json()
    assert resp_json["status_code"] == 400
    assert resp_json["message"] == "Error: Debe especificar la forma de pago"
    assert resp_json["detalle_compra"] is None
    assert resp_json["envio_de_mail"] == "NO_ENVIADO"
def test_post_validar_compra_entradas_falta_dato_entradas():
    compra_data_incompleta = {
                    "forma_pago": "tarjeta",
                    "fecha_visita": "2024-12-15",
                    "id_usuario": 1
                }

    resp = client.post("/validar-compra-entradas", json=compra_data_incompleta)
    resp_json = resp.json()
    assert resp_json["status_code"] == 400
    assert resp_json["message"] == "Error: Debe especificar las entradas a comprar"
    assert resp_json["detalle_compra"] is None
    assert resp_json["envio_de_mail"] == "NO_ENVIADO"
def test_post_validar_compra_entradas_falta_dato_id_usuario():
    compra_data_incompleta = {
                    "forma_pago": "tarjeta",
                    "entradas": [
                        {
                            "edad_visitante": 30,
                            "tipo_pase": "VIP",
                            "precio": 100.0
                        }
                    ],  
                    "fecha_visita": "2024-12-15"
                }

    resp = client.post("/validar-compra-entradas", json=compra_data_incompleta)
    resp_json = resp.json()
    assert resp_json["status_code"] == 400
    assert resp_json["message"] == "Error: Debe especificar el ID del usuario"
    assert resp_json["detalle_compra"] is None
    assert resp_json["envio_de_mail"] == "NO_ENVIADO"
def test_post_validar_compra_entradas_falta_dato_fecha_visita():
    compra_data_incompleta = {
                    "forma_pago": "tarjeta",
                    "entradas": [
                        {
                            "edad_visitante": 30,
                            "tipo_pase": "VIP",
                            "precio": 100.0
                        }
                    ],
                    "id_usuario": 1
                }
    resp = client.post("/validar-compra-entradas", json=compra_data_incompleta)
    resp_json = resp.json()
    assert resp_json["status_code"] == 400
    assert resp_json["message"] == "Error: Debe especificar la fecha de visita"
    assert resp_json["detalle_compra"] is None
    assert resp_json["envio_de_mail"] == "NO_ENVIADO"


# TODO -> ESTE ES DE INTEGRACION, Testear para usuario inexistente
def test_post_validar_compra_entradas_usuario_inexistente():
    compra_data = {
                    "forma_pago": "tarjeta",
                    "entradas": [
                        {
                            "edad_visitante": 30,
                            "tipo_pase": "VIP",
                            "precio": 100.0
                        }
                    ],
                    "fecha_visita": "2025-12-15",
                    "id_usuario": 9999  # ID de usuario inexistente
                }

    resp = client.post("/validar-compra-entradas", json=compra_data)
    resp_json = resp.json()
    assert resp_json["status_code"] == 400
    assert resp_json["message"] == "Error: Error al validar usuario: El usuario no está registrado"
    assert resp_json["detalle_compra"] is None


# Probar comprar una entrada indicando la fecha de visita dentro de los días disponibles, una
# cantidad de entradas menor a 10, la edad de todos los visitantes, el tipo de pase, la forma de
# pago con tarjeta mediante Mercado pago y recepción del mail de confirmación (pasa)

def test_validar_compra_tarjeta():
    forma_pago = "tarjeta"
    entradas = [
        Entrada(str(devolver_fecha_dia_abierto()), edad_visitante=20, tipo_pase="Regular", precio=1000.0),
        Entrada(str(devolver_fecha_dia_abierto()), edad_visitante=15, tipo_pase="VIP", precio=2000.0)
    ]
    usuario_id = 1
    fecha_visita = "2025-12-20"
    compra, cant_entradas, fecha_compra, estado_envio_mail = service.validar_compra(forma_pago, entradas, usuario_id)

    assert compra is not None
    assert cant_entradas == 2
    assert fecha_compra == date.today()
    assert estado_envio_mail == "PENDIENTE"
    assert compra.usuario.id_usuario == 1
    assert compra.pago is not None
    assert compra.pago.monto == 4700.5
    assert compra.pago.forma_pago == "tarjeta"
    assert compra.pago.estado_pago == "PAGO_PENDIENTE_POR_MERCADO_PAGO"
    assert compra.pago.codigo_pago == 0
def test_validar_compra_efectivo():
    forma_pago = "efectivo"
    entradas = [
        Entrada(str(devolver_fecha_dia_abierto()), edad_visitante=20, tipo_pase="Regular", precio=1000.0),
        Entrada(str(devolver_fecha_dia_abierto()), edad_visitante=15, tipo_pase="VIP", precio=2000.0)
    ]
    usuario_id = 1
    fecha_visita = "2025-12-20"
    compra, cant_entradas, fecha_compra, estado_envio_mail = service.validar_compra(forma_pago, entradas, usuario_id)

    assert compra is not None
    assert cant_entradas == 2
    assert fecha_compra == date.today()
    assert estado_envio_mail == "ENVIADO"
    assert compra.usuario.id_usuario == usuario_id
    assert compra.pago is not None
    assert compra.pago.monto == 4700.5
    assert compra.pago.forma_pago == "efectivo"
    assert compra.pago.estado_pago == "PAGO_A_REALIZAR_EN_CAJA"
    assert compra.pago.codigo_pago == 0

# Validamos metodos derivados del metodo procesar_compra

def test_validar_forma_pago_valida():
    assert service._validar_forma_pago("Efectivo") == "efectivo"
    assert service._validar_forma_pago("Tarjeta") == "tarjeta"
def test_validar_forma_pago_invalida():
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_forma_pago("Cheque")
    assert str(excinfo.value) == "Debe seleccionar una forma de pago válida: efectivo, tarjeta"

def test_validar_fecha_visita_dia_valido():
    # Buscar el próximo día válido (lunes a sábado)
    fecha_valida = devolver_fecha_dia_abierto()
    assert service._validar_fecha_visita(str(fecha_valida)) == date.fromisoformat(str(fecha_valida))
def test_validar_fecha_visita_pasada():
    fecha_pasada = (date.today() - timedelta(days=1))
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_fecha_visita(str(fecha_pasada))
    assert str(excinfo.value) == "La fecha de visita no puede ser anterior a hoy"
def test_validar_fecha_visita_dia_cerrado():
    # Buscar el próximo domingo (día cerrado)
    dias_abiertos = service.dias_abierto
    # dias_abiertos = [0,1,2,3,4,5,6]  # Lunes a Sábado

    dias_adelante = 1
    if len(dias_abiertos) == 7:
        pytest.skip("No hay días cerrados configurados en el servicio.")
    while True:
        fecha_futura = date.today() + timedelta(days=dias_adelante)
        if fecha_futura.weekday() not in dias_abiertos:  # Domingo
            break
        dias_adelante += 1
    
    fecha_cerrada = fecha_futura
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_fecha_visita(str(fecha_cerrada))
    assert str(excinfo.value) == "El parque está cerrado en la fecha seleccionada"
 
def test_validar_cantidad_entradas_valida():
    assert service._validar_cantidad_entradas(5) is True
def test_validar_cantidad_entradas_cero():
    cant_min_entradas = service.min_entradas
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_cantidad_entradas(0)
    assert str(excinfo.value) == f"Debe solicitar al menos {cant_min_entradas} entrada"
def test_validar_cantidad_entradas_exceso():

    with pytest.raises(ValidacionError) as excinfo:
        service._validar_cantidad_entradas(11)
    assert str(excinfo.value) == "La cantidad de entradas no puede ser mayor a 10"

# ESTOS NO SE COMMITEAN AUN
# LOS TESTS DE INTEGRACION DEBEN HACERSE LUEGO DE ALGUNAS IMPLEMENTACIONES, PRIMERO HACEMOS LOS UNITARIOS DE ARRIBA
# TODO este es de INTEGRACION

def test_valida_usuario_registrado():
    id_usuario = 1
    resultado = service._validar_usuario_registrado(id_usuario)
    assert isinstance(resultado, Usuario)
    assert resultado.id_usuario == id_usuario
def test_valida_usuario_registrado_id_invalido():
    usuario_id_invalido = -1
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_usuario_registrado(usuario_id_invalido)
    assert str(excinfo.value) == "ID de usuario inválido"

def test_validar_entrada_valida():
    entrada_valida = Entrada(fecha_visita=str(devolver_fecha_dia_abierto()), edad_visitante=25, tipo_pase="VIP", precio=2000.0)
    assert service._validar_entrada_completa(entrada_valida) is True
def test_validar_entrada_edad_negativa():
    entrada_invalida = Entrada(fecha_visita=str(devolver_fecha_dia_abierto()), edad_visitante=-5, tipo_pase="Regular", precio=1000.0)
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_entrada_completa(entrada_invalida)
    assert str(excinfo.value) == "La edad del visitante no puede ser negativa"
def test_validar_entrada_tipo_pase_invalido():
    entrada_invalida = Entrada(fecha_visita=str(devolver_fecha_dia_abierto()), edad_visitante=30, tipo_pase="SuperVIP", precio=150.0)
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_entrada_completa(entrada_invalida)
    assert str(excinfo.value) == "El tipo de pase debe ser uno de: VIP, Regular"
def test_validar_entrada_precio_negativo():
    entrada_invalida = Entrada(fecha_visita=str(devolver_fecha_dia_abierto()), edad_visitante=20, tipo_pase="Regular", precio=-10.0)
    with pytest.raises(ValidacionError) as excinfo:
        service._validar_entrada_completa(entrada_invalida)
    assert str(excinfo.value) == "El precio de la entrada no puede ser negativo"


# de utilidad, pushear al principio
def devolver_fecha_dia_abierto():
    fecha = date.today()
    while fecha.weekday() == 6:  # Mientras sea domingo
        fecha += timedelta(days=1)
    return fecha
