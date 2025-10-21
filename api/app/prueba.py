
from .usuario import Usuario
from .repositorioCompraEntradas import RepositorioCompraEntradas

def main():
    repositorio_bd = RepositorioCompraEntradas()
    # usuario = Usuario("Juan", "Pérez", "juan@example.com", "password123")
    # print(f"Usuario antes de crear en BD: {usuario}")
    # usuario = repositorio_bd.crear_usuario(usuario)
    # print(f"Usuario creado: {usuario}")
    usuario_obtenido = repositorio_bd.obtener_usuario_por_id(4)
    print(f"Usuario obtenido: {usuario_obtenido}")

if __name__ == "__main__":
    main()