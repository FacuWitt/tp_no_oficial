from fastapi.testclient import TestClient
from app.api import app
import pytest
from datetime import date, timedelta
from app.usuario import Usuario
from app.entrada import Entrada
from app.validacionError import ValidacionError
from app.compra import Compra
from app.servicioCompraEntradas import ServicioCompraEntradas

client = TestClient(app)
service = ServicioCompraEntradas()

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
"""
# testear para usuario inexistente
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
    assert resp.status_code == 400
    resp_json = resp.json()
    assert resp_json["message"] == "Error: El usuario con ese ID no está registrado"
    assert resp_json["detalle_compra"] is None


# Probar comprar una entrada indicando la fecha de visita dentro de los días disponibles, una
# cantidad de entradas menor a 10, la edad de todos los visitantes, el tipo de pase, la forma de
# pago con tarjeta mediante Mercado pago y recepción del mail de confirmación (pasa)

def test_validar_compra_tarjeta():
    forma_pago = "tarjeta"
    entradas = [
        Entrada(devolver_fecha_dia_abierto(), edad_visitante=20, tipo_pase="Regular", precio=50.0),
        Entrada(devolver_fecha_dia_abierto(), edad_visitante=15, tipo_pase="VIP", precio=80.0)
    ]
    usuario_id = 1
    fecha_visita = "2025-12-20"
    resultado = service.validar_compra(forma_pago, entradas, usuario_id, fecha_visita)
    assert resultado.estado_compra == "COMPRA_VALIDADA"
    assert resultado.compra is not None
    assert resultado.compra.fecha == date.today()
    assert resultado.compra.forma_pago == "tarjeta"
    assert len(resultado.compra.entradas) == 2
    assert resultado.compra.precio_total == 130.0
    assert resultado.compra.usuario.usuario_id == usuario_id
    assert resultado.pago is not None
    assert resultado.pago.monto == 130.0
    assert resultado.pago.forma_pago == "tarjeta"
    assert resultado.pago.estado_pago == "PAGO_PENDIENTE_POR_MERCADO_PAGO"
    assert resultado.pago.codigo_pago == 0
def test_validar_compra_efectivo():
    forma_pago = "efectivo"
    entradas = [
        Entrada(devolver_fecha_dia_abierto(), edad_visitante=20, tipo_pase="Regular", precio=50.0),
        Entrada(devolver_fecha_dia_abierto(), edad_visitante=15, tipo_pase="VIP", precio=80.0)
    ]
    usuario_id = 1
    fecha_visita = "2025-12-20"
    resultado = service.validar_compra(forma_pago, entradas, usuario_id, fecha_visita)
    assert resultado.estado_compra == "COMPRA_VALIDADA"
    assert resultado.compra is not None
    assert resultado.compra.fecha == date.today()
    assert resultado.compra.forma_pago == "efectivo"
    assert len(resultado.compra.entradas) == 2
    assert resultado.compra.precio_total == 130.0
    assert resultado.compra.usuario.usuario_id == usuario_id
    assert resultado.pago is not None
    assert resultado.pago.monto == 130.0
    assert resultado.pago.forma_pago == "efectivo"
    assert resultado.pago.estado_pago == "PAGO_A_REALIZAR_EN_CAJA"
    assert resultado.pago.codigo_pago == 0

# Validamos metodos derivados del metodo procesar_compra

def test_validar_forma_pago_valida():
    assert service.validar_forma_pago("Efectivo") == "efectivo"
    assert service.validar_forma_pago("Tarjeta") == "tarjeta"
def test_validar_forma_pago_invalida():
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_forma_pago("Cheque")
    assert str(excinfo.value) == "Debe seleccionar una forma de pago válida (Efectivo o Tarjeta)"

def test_validar_fecha_visita_dia_valido():
    # Buscar el próximo día válido (lunes a sábado)
    fecha_valida = devolver_fecha_dia_abierto()
    assert service.validar_fecha_visita(str(fecha_valida)) == date.fromisoformat(fecha_valida)
def test_validar_fecha_visita_pasada():
    fecha_pasada = (date.today() - timedelta(days=1))
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_fecha_visita(str(fecha_pasada))
    assert str(excinfo.value) == "La fecha de visita no puede ser anterior a hoy"
def test_validar_fecha_visita_dia_cerrado():
    # Buscar el próximo domingo (día cerrado)
    dias_adelante = 1
    while True:
        fecha_futura = date.today() + timedelta(days=dias_adelante)
        if fecha_futura.weekday() == 6:  # Domingo
            break
        dias_adelante += 1
    
    domingo_cerrado = fecha_futura
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_fecha_visita(str(domingo_cerrado))
    assert str(excinfo.value) == "El parque está cerrado en la fecha seleccionada"

def test_valida_usuario_registrado():
    usuario_id = 1
    resultado = service.validar_usuario_registrado(usuario_id)
    assert isinstance(resultado, Usuario)
    assert resultado.usuario_id == usuario_id
def test_valida_usuario_registrado_id_invalido():
    usuario_id_invalido = -1
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_usuario_registrado(usuario_id_invalido)
    assert str(excinfo.value) == "El usuario con ese ID no está registrado"
    
def test_validar_cantidad_entradas_valida():
    assert service.validar_cantidad_entradas(5) is True
def test_validar_cantidad_entradas_cero():
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_cantidad_entradas(0)
    assert str(excinfo.value) == "Debe solicitar al menos una entrada"
def test_validar_cantidad_entradas_exceso():
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_cantidad_entradas(11)
    assert str(excinfo.value) == "La cantidad de entradas no puede ser mayor a 10"

def test_validar_entrada_valida():
    entrada_valida = Entrada(fecha_visita=devolver_fecha_dia_abierto(), edad_visitante=25, tipo_pase="VIP", precio=100.0)
    assert service.validar_entrada(entrada_valida) is True
def test_validar_entrada_edad_negativa():
    entrada_invalida = Entrada(fecha_visita=devolver_fecha_dia_abierto(), edad_visitante=-5, tipo_pase="Regular", precio=50.0)
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_entrada(entrada_invalida)
    assert str(excinfo.value) == "La edad del visitante no puede ser negativa"
def test_validar_entrada_tipo_pase_invalido():
    entrada_invalida = Entrada(fecha_visita=devolver_fecha_dia_abierto(), edad_visitante=30, tipo_pase="SuperVIP", precio=150.0)
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_entrada(entrada_invalida)
    assert str(excinfo.value) == "El tipo de pase no es válido"
def test_validar_entrada_precio_negativo():
    entrada_invalida = Entrada(fecha_visita=devolver_fecha_dia_abierto(), edad_visitante=20, tipo_pase="Regular", precio=-10.0)
    with pytest.raises(ValidacionError) as excinfo:
        service.validar_entrada(entrada_invalida)
    assert str(excinfo.value) == "El precio de la entrada no puede ser negativo"

def devolver_fecha_dia_abierto():
    fecha = date.today()
    while fecha.weekday() == 6:  # Mientras sea domingo
        fecha += timedelta(days=1)
    return fecha

"""