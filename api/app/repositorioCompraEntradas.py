# from datetime import date
# import sqlite3 
# import os

# # Ruta absoluta al archivo de la base de datos
# current_dir = os.path.dirname(os.path.abspath(__file__))
# path_db = os.path.join(current_dir, '..', '..', 'db', 'app.db')

# from .usuario import Usuario
# from .compra import Compra
# from .pago import Pago
# from .entrada import Entrada


# class RepositorioCompraEntradas:
#     def __init__(self):
#         self.path_db = path_db

#         if not os.path.exists(self.path_db):
#             print(f"⚠️  ADVERTENCIA: Base de datos no encontrada en: {self.path_db}")
#         if os.path.exists(self.path_db):
#             try:
#                 with sqlite3.connect(self.path_db) as conn:
#                     cursor = conn.cursor()
#                     cursor.execute("SELECT 1")
#                     print(f"✅ Conexión exitosa a BD: {self.path_db}")
#             except sqlite3.Error as e:
#                 print(f"❌ Error de conexión a BD: {e}")
#                 raise ConnectionError(f"No se puede conectar a la base de datos: {e}")

#     def crear_usuario(self, usuario: Usuario):
#         try:
#             with sqlite3.connect(self.path_db) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     INSERT INTO Usuario (nombre, apellido, mail, contraseña)
#                     VALUES (?, ?, ?, ?)
#                 ''', (usuario.nombre, usuario.apellido, usuario.mail, usuario.contraseña))
#                 conn.commit()
#                 usuario.id_usuario = cursor.lastrowid
#                 return usuario
#         except sqlite3.Error as e:
#             print(f"Error al crear usuario: {e}")
#             raise


#     def obtener_usuario_por_id(self, id_usuario: int):
#         try:
#             with sqlite3.connect(self.path_db) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     SELECT id_usuario, nombre, apellido, mail, contraseña
#                     FROM Usuario
#                     WHERE id_usuario = ?
#                 ''', (id_usuario,))
#                 usuario_bd = cursor.fetchone()
                
#                 if usuario_bd:
#                     usuario_encontrado = Usuario(
#                         nombre=usuario_bd[1],
#                         apellido=usuario_bd[2],
#                         mail=usuario_bd[3],
#                         contraseña=usuario_bd[4]
#                     )
#                     usuario_encontrado.id_usuario = usuario_bd[0]
#                     return usuario_encontrado
#                 return None
#         except sqlite3.Error as e:
#             print(f"Error al obtener usuario: {e}")
#             raise
    
#     def crear_pago(self, pago: Pago):
#         try:
#             with sqlite3.connect(self.path_db) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     INSERT INTO Pago (forma_pago, estado_pago, codigo_pago, monto)
#                     VALUES (?, ?, ?, ?)
#                 ''', (pago.forma_pago, pago.estado_pago, pago.codigo_pago, pago.monto))
#                 conn.commit()
#                 pago.id_pago = cursor.lastrowid
#                 return pago
#         except sqlite3.Error as e:
#             print(f"Error al crear pago: {e}")
#             raise

#     def crear_entradas(self, entradas: list[Entrada], id_compra: int):
#         try:
#             with sqlite3.connect(self.path_db) as conn:
#                 cursor = conn.cursor()
#                 for entrada in entradas:
#                     cursor.execute('''
#                         INSERT INTO Entrada (id_compra, fecha_visita, tipo_pase, edad_visitante, precio)
#                         VALUES (?, ?, ?, ?, ?)''', 
#                         (id_compra, entrada.fecha_visita, entrada.tipo_pase, entrada.edad_visitante, entrada.precio))
#                     entrada.id_entrada = cursor.lastrowid
#                 conn.commit()
#                 return entradas
#         except sqlite3.Error as e:
#             print(f"Error al crear entradas: {e}")
#             raise

#     def crear_compra(self, compra: Compra):
#         pago_de_compra = self.crear_pago(compra.pago)
#         compra.pago.id_pago = pago_de_compra.id_pago
#         try:
#             with sqlite3.connect(self.path_db) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     INSERT INTO Compra (fecha, precio_total, id_usuario, id_pago)
#                     VALUES (?, ?, ?, ?)
#                 ''', (compra.fecha.isoformat(), compra.precio_total, compra.usuario.id_usuario, compra.pago.id_pago))
#                 conn.commit()
#                 compra.id_compra = cursor.lastrowid
#                 entradas = self.crear_entradas(compra.entradas, compra.id_compra)
#                 compra.entradas = entradas
#                 return compra
#         except sqlite3.Error as e:
#             print(f"Error al crear compra: {e}")
#             raise
#         except sqlite3.Error as e:
#             print(f"Error al crear compra: {e}")
#             raise

#     def obtener_compra_por_id(self, id_compra: int):
#         try:
#             with sqlite3.connect(self.path_db) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     SELECT id_compra, fecha, precio_total, id_usuario, id_pago
#                     FROM Compra
#                     WHERE id_compra = ?
#                 ''', (id_compra,))
#                 compra_bd = cursor.fetchone()
                
#                 if not compra_bd:
#                     return None
                
#                 cursor.execute('''
#                     SELECT id_pago, forma_pago, estado_pago, codigo_pago, monto
#                     FROM Pago
#                     WHERE id_pago = ?
#                 ''', (compra_bd[4],))
#                 pago_bd = cursor.fetchone()
                
#                 pago = Pago(
#                     forma_pago=pago_bd[1],
#                     estado_pago=pago_bd[2],
#                     codigo_pago=pago_bd[3],
#                     monto=pago_bd[4]
#                 )
#                 pago.id_pago = pago_bd[0]
                
#                 cursor.execute('''
#                     SELECT id_usuario, nombre, apellido, mail, contraseña
#                     FROM Usuario
#                     WHERE id_usuario = ?
#                 ''', (compra_bd[3],))
#                 usuario_bd = cursor.fetchone()
                
#                 usuario = Usuario(
#                     nombre=usuario_bd[1],
#                     apellido=usuario_bd[2],
#                     mail=usuario_bd[3],
#                     contraseña=usuario_bd[4]
#                 )
#                 usuario.id_usuario = usuario_bd[0]
                
#                 cursor.execute('''
#                     SELECT id_entrada, fecha_visita, tipo_pase, edad_visitante, precio
#                     FROM Entrada
#                     WHERE id_compra = ?
#                 ''', (id_compra,))
#                 entradas_bd = cursor.fetchall()
                
#                 entradas = []
#                 for entrada_row in entradas_bd:
#                     entrada = Entrada(
#                         fecha_visita=entrada_row[1],
#                         tipo_pase=entrada_row[2],
#                         edad_visitante=entrada_row[3],
#                         precio=entrada_row[4]
#                     )
#                     entrada.id_entrada = entrada_row[0]
#                     entradas.append(entrada)
                
#                 compra = Compra(
#                     entradas=entradas,
#                     usuario=usuario,
#                     pago=pago
#                 )
#                 compra.id_compra = compra_bd[0]
#                 compra.fecha = date.fromisoformat(compra_bd[1])
#                 compra.precio_total = compra_bd[2]
                
#                 return compra
#         except sqlite3.Error as e:
#             print(f"Error al obtener compra: {e}")
#             raise

#     def actualizar_pago_compra(self, compra: Compra):
#         try:
#             with sqlite3.connect(self.path_db) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     UPDATE Pago
#                     SET forma_pago = ?, estado_pago = ?, codigo_pago = ?, monto = ?
#                     WHERE id_pago = ?
#                 ''', (compra.pago.forma_pago, compra.pago.estado_pago, compra.pago.codigo_pago, compra.pago.monto, compra.pago.id_pago))
#                 conn.commit()
#                 return compra
#         except sqlite3.Error as e:
#             print(f"Error al actualizar pago de compra: {e}")
#             raise

from datetime import date
import sqlite3 
import os
from contextlib import contextmanager

# Ruta absoluta al archivo de la base de datos
current_dir = os.path.dirname(os.path.abspath(__file__))
path_db = os.path.join(current_dir, '..', '..', 'db', 'app.db')

from .usuario import Usuario
from .compra import Compra
from .pago import Pago
from .entrada import Entrada


class RepositorioCompraEntradas:
    def __init__(self):
        self.path_db = path_db
        self._verificar_conexion()

    def _verificar_conexion(self):
        """Método privado para verificar la conexión a la BD"""
        if not os.path.exists(self.path_db):
            print(f"⚠️  ADVERTENCIA: Base de datos no encontrada en: {self.path_db}")
            return
        
        try:
            with sqlite3.connect(self.path_db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                print(f"✅ Conexión exitosa a BD: {self.path_db}")
        except sqlite3.Error as e:
            print(f"❌ Error de conexión a BD: {e}")
            raise ConnectionError(f"No se puede conectar a la base de datos: {e}")

    @contextmanager
    def _get_connection(self):
        """Context manager para manejo seguro de conexiones"""
        conn = None
        try:
            conn = sqlite3.connect(self.path_db)
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def crear_usuario(self, usuario: Usuario):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Usuario (nombre, apellido, mail, contraseña)
                    VALUES (?, ?, ?, ?)
                ''', (usuario.nombre, usuario.apellido, usuario.mail, usuario.contraseña))
                conn.commit()
                usuario.id_usuario = cursor.lastrowid
                return usuario
        except sqlite3.Error as e:
            print(f"Error al crear usuario: {e}")
            raise

    def obtener_usuario_por_id(self, id_usuario: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id_usuario, nombre, apellido, mail, contraseña
                    FROM Usuario
                    WHERE id_usuario = ?
                ''', (id_usuario,))
                usuario_bd = cursor.fetchone()
                
                if not usuario_bd:
                    return None
                    
                usuario_encontrado = Usuario(
                    nombre=usuario_bd[1],
                    apellido=usuario_bd[2],
                    mail=usuario_bd[3],
                    contraseña=usuario_bd[4]
                )
                usuario_encontrado.id_usuario = usuario_bd[0]
                return usuario_encontrado
        except sqlite3.Error as e:
            print(f"Error al obtener usuario: {e}")
            raise
    
    def crear_pago(self, pago: Pago, conn=None):
        """Permite usar una conexión existente para transacciones"""
        cursor = conn.cursor() if conn else None
        
        if not conn:
            try:
                with self._get_connection() as connection:
                    return self._ejecutar_crear_pago(pago, connection)
            except sqlite3.Error as e:
                print(f"Error al crear pago: {e}")
                raise
        else:
            return self._ejecutar_crear_pago(pago, conn)

    def _ejecutar_crear_pago(self, pago: Pago, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Pago (forma_pago, estado_pago, codigo_pago, monto)
            VALUES (?, ?, ?, ?)
        ''', (pago.forma_pago, pago.estado_pago, pago.codigo_pago, pago.monto))
        pago.id_pago = cursor.lastrowid
        return pago

    def crear_entradas(self, entradas: list[Entrada], id_compra: int, conn=None):
        """Permite usar una conexión existente para transacciones"""
        if not conn:
            try:
                with self._get_connection() as connection:
                    return self._ejecutar_crear_entradas(entradas, id_compra, connection)
            except sqlite3.Error as e:
                print(f"Error al crear entradas: {e}")
                raise
        else:
            return self._ejecutar_crear_entradas(entradas, id_compra, conn)

    def _ejecutar_crear_entradas(self, entradas: list[Entrada], id_compra: int, conn):
        cursor = conn.cursor()
        for entrada in entradas:
            cursor.execute('''
                INSERT INTO Entrada (id_compra, fecha_visita, tipo_pase, edad_visitante, precio)
                VALUES (?, ?, ?, ?, ?)''', 
                (id_compra, entrada.fecha_visita, entrada.tipo_pase, entrada.edad_visitante, entrada.precio))
            entrada.id_entrada = cursor.lastrowid
        return entradas

    def crear_compra(self, compra: Compra):
        """Transacción atómica para crear compra completa"""
        try:
            with self._get_connection() as conn:
                # Crear pago dentro de la transacción
                pago_de_compra = self.crear_pago(compra.pago, conn)
                compra.pago.id_pago = pago_de_compra.id_pago
                
                # Crear la compra
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Compra (fecha, precio_total, id_usuario, id_pago)
                    VALUES (?, ?, ?, ?)
                ''', (compra.fecha.isoformat(), compra.precio_total, compra.usuario.id_usuario, compra.pago.id_pago))
                compra.id_compra = cursor.lastrowid
                
                # Crear entradas dentro de la transacción
                entradas = self.crear_entradas(compra.entradas, compra.id_compra, conn)
                compra.entradas = entradas
                
                conn.commit()
                return compra
        except sqlite3.Error as e:
            print(f"Error al crear compra: {e}")
            raise

    def obtener_compra_por_id(self, id_compra: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Query optimizada con JOINs
                cursor.execute('''
                    SELECT 
                        c.id_compra, c.fecha, c.precio_total,
                        u.id_usuario, u.nombre, u.apellido, u.mail, u.contraseña,
                        p.id_pago, p.forma_pago, p.estado_pago, p.codigo_pago, p.monto
                    FROM Compra c
                    JOIN Usuario u ON c.id_usuario = u.id_usuario
                    JOIN Pago p ON c.id_pago = p.id_pago
                    WHERE c.id_compra = ?
                ''', (id_compra,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                # Crear objetos con los datos obtenidos
                usuario = Usuario(
                    nombre=row[4],
                    apellido=row[5],
                    mail=row[6],
                    contraseña=row[7]
                )
                usuario.id_usuario = row[3]
                
                pago = Pago(
                    forma_pago=row[9],
                    estado_pago=row[10],
                    codigo_pago=row[11],
                    monto=row[12]
                )
                pago.id_pago = row[8]
                
                # Obtener entradas
                cursor.execute('''
                    SELECT id_entrada, fecha_visita, tipo_pase, edad_visitante, precio
                    FROM Entrada
                    WHERE id_compra = ?
                ''', (id_compra,))
                
                entradas = []
                for entrada_row in cursor.fetchall():
                    entrada = Entrada(
                        fecha_visita=entrada_row[1],
                        tipo_pase=entrada_row[2],
                        edad_visitante=entrada_row[3],
                        precio=entrada_row[4]
                    )
                    entrada.id_entrada = entrada_row[0]
                    entradas.append(entrada)
                
                compra = Compra(
                    entradas=entradas,
                    usuario=usuario,
                    pago=pago
                )
                compra.id_compra = row[0]
                compra.fecha = date.fromisoformat(row[1])
                compra.precio_total = row[2]
                
                return compra
        except sqlite3.Error as e:
            print(f"Error al obtener compra: {e}")
            raise

    def actualizar_pago_compra(self, compra: Compra):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE Pago
                    SET forma_pago = ?, estado_pago = ?, codigo_pago = ?, monto = ?
                    WHERE id_pago = ?
                ''', (compra.pago.forma_pago, compra.pago.estado_pago, compra.pago.codigo_pago, compra.pago.monto, compra.pago.id_pago))
                conn.commit()
                return compra
        except sqlite3.Error as e:
            print(f"Error al actualizar pago de compra: {e}")
            raise