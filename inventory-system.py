import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class Producto:
    def __init__(self, codigo: int, nombre: str, precio: float, cantidad: int, stock_minimo: int = 5):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.stock_minimo = stock_minimo
        self.ventas = 0

def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "stock_minimo": self.stock_minimo,
            "ventas": self.ventas
        }
    def __str__(self) -> str:
        return f"Código: {self.codigo:04d} | Nombre: {self.nombre} | Precio: ${self.precio:.2f} | Cantidad: {self.cantidad}" 
    
class SistemaInventario:
    def __init__(self):
        self.productos: Dict[int, Producto] = {}
        self.cargar_datos()

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def guardar_datos(self):
    """Guarda los datos del inventario en un archivo JSON."""
    try:
        with open("inventario.json", "w", encoding="utf-8") as archivo:
            datos = [producto.__dict__ for producto in self.productos.values()]
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print("\nDatos guardados exitosamente.")
    except Exception as e:
        print(f"\nError al guardar los datos: {e}")
        
    def cargar_datos(self):
    """Carga los datos del inventario desde un archivo JSON."""
    if not os.path.exists("inventario.json"):
        print("\nNo se encontró un archivo de datos. Se iniciará con un inventario vacío.")
        return

    try:
        with open("inventario.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            for item in datos:
                producto = Producto(
                    codigo=item["codigo"],
                    nombre=item["nombre"],
                    precio=item["precio"],
                    cantidad=item["cantidad"],
                    stock_minimo=item["stock_minimo"]
                )
                producto.ventas = item.get("ventas", 0)
                self.productos[producto.codigo] = producto
        print("\nDatos cargados exitosamente.")
    except Exception as e:
        print(f"\nError al cargar los datos: {e}")
        
    def validar_codigo(self, codigo_str: str) -> tuple[bool, Optional[int]]:
        try:
            codigo = int(codigo_str)
            if codigo <= 0:
                print("\n¡Error! El código debe ser un número positivo.")
                return False, None
            if codigo in self.productos:
                print("\n¡Error! Este código de producto ya fue ingresado.")
                return False, None
            return True, codigo
        except ValueError:
            print("\n¡Error! El código debe ser un número entero.")
            return False, None

    def validar_codigo_existente(self, codigo_str: str) -> tuple[bool, Optional[int]]:
        try:
            codigo = int(codigo_str)
            if codigo <= 0:
                print("\n¡Error! El código debe ser un número positivo.")
                return False, None
            if codigo not in self.productos:
                print("\n¡Error! El código no existe en el inventario.")
                return False, None
            return True, codigo
        except ValueError:
            print("\n¡Error! El código debe ser un número entero.")
            return False, None

    def validar_nombre(self, nombre: str) -> bool:
        if any(nombre.lower() == producto.nombre.lower() for producto in self.productos.values()):
            print("\n¡Error! Ya existe un producto con el mismo nombre en el inventario.")
            return False
        return True

    def agregar_producto(self, codigo: int, nombre: str, precio: float, cantidad: int, stock_minimo: int = 5) -> bool:
    if codigo in self.productos:
        print("\n¡Error! El código ya existe en el inventario.")
        return False

    if not self.validar_nombre(nombre):
        return False

    self.productos[codigo] = Producto(codigo, nombre, precio, cantidad, stock_minimo)
    print("\n¡Producto agregado exitosamente!")
    self.guardar_datos()  # Guardar cambios
    return True

    def actualizar_producto(self, codigo: int, nombre: Optional[str] = None, precio: Optional[float] = None, cantidad: Optional[int] = None) -> bool:
        if codigo not in self.productos:
            print("\n¡Error! El producto no existe en el inventario.")
            return False

        producto = self.productos[codigo]
        if nombre:
            if not self.validar_nombre(nombre):
                return False
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if cantidad is not None:
            producto.cantidad += cantidad

        self.guardar_datos()
        print("\n¡Producto actualizado exitosamente!")
        return True

    def eliminar_producto(self, codigo: int) -> bool:
        if codigo not in self.productos:
            print("\n¡Error! El producto no existe en el inventario.")
            return False

        del self.productos[codigo]
        self.guardar_datos()
        print("\n¡Producto eliminado exitosamente!")
        return True

    def buscar_producto(self, termino: str) -> List[Producto]:
        resultados = []
        termino = termino.lower()
        for producto in self.productos.values():
            if str(producto.codigo) == termino or termino in producto.nombre.lower():
                resultados.append(producto)
        return resultados

    def verificar_stock_bajo(self) -> List[Producto]:
        return [p for p in self.productos.values() if p.cantidad <= p.stock_minimo]

    def mostrar_alerta_stock_bajo(self):
        productos_bajo_stock = self.verificar_stock_bajo()
        if productos_bajo_stock:
            print("\n¡ALERTA! Los siguientes productos están por debajo del stock mínimo:")
            print("=" * 70)
            print(f"{'Código':<10}{'Nombre':<30}{'Stock Actual':<15}{'Stock Mínimo':<15}")
            print("-" * 70)
            for producto in productos_bajo_stock:
                print(f"{producto.codigo:<10}{producto.nombre:<30}{producto.cantidad:<15}{producto.stock_minimo:<15}")
            print("=" * 70)
            print("Se recomienda realizar un reabastecimiento lo antes posible.")

    def registrar_venta(self, codigo: int, cantidad: int) -> bool:
        if codigo not in self.productos:
            print("\n¡Error! El producto no existe en el inventario.")
            return False

        producto = self.productos[codigo]
        if producto.cantidad < cantidad:
            print("\n¡Error! No hay suficiente stock disponible.")
            return False

        producto.cantidad -= cantidad
        producto.ventas += cantidad
        self.guardar_datos()
        print("\n¡Venta registrada exitosamente!")
        return True

    def generar_reporte(self) -> str:
        total_productos = len(self.productos)
        valor_total = sum(p.precio * p.cantidad for p in self.productos.values())
        productos_bajo_stock = self.verificar_stock_bajo()
        
        todos_productos_ordenados = sorted(self.productos.values(), key=lambda x: x.ventas, reverse=True)
        productos_mas_vendidos = [p for p in todos_productos_ordenados if p.ventas > 0][:5]
        promedio_ventas = sum(p.ventas for p in self.productos.values()) / total_productos if total_productos > 0 else 0
        productos_menos_vendidos = [p for p in self.productos.values() if p.ventas <= promedio_ventas]

        # Definición de anchos fijos para todo el reporte
        ancho_linea = 76
        col_codigo = 10
        col_nombre = 30
        col_cantidad = 12
        col_precio = 12
        col_ventas = 12
        col_medida = 12

        # Crear el título principal
        titulo_principal = f"REPORTE DE INVENTARIO ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
        reporte = "\n" + titulo_principal.center(ancho_linea) + "\n"
        reporte += "=" * ancho_linea + "\n"
        
        # Sección de resumen general
        reporte += "RESUMEN GENERAL SISTEMA DE INVENTARIO".center(ancho_linea) + "\n"
        reporte += "=" * ancho_linea + "\n"

        # Columnas para el resumen ajustadas para una sola línea
        col_info = 38  # Columna para información de productos
        col_valor = 38  # Columna para valor del inventario

        # Encabezados de la tabla de resumen
        reporte += f"{'Total de Productos'.center(col_info)}{'Valor del Inventario ($)'.center(col_valor)}\n"
        reporte += "-" * ancho_linea + "\n"
        
        # Datos del resumen en una sola línea
        reporte += f"{str(total_productos).center(col_info)}{f'${valor_total:,.2f}'.center(col_valor)}\n"

        # Sección de productos con stock bajo
        reporte += "\n" + "PRODUCTOS CON STOCK BAJO".center(ancho_linea) + "\n"
        reporte += "=" * ancho_linea + "\n"

        reporte += f"{'Código'.ljust(col_codigo)}{'Nombre'.ljust(col_nombre)}"
        reporte += f"{'Cantidad'.ljust(col_cantidad)}{'Mínimo'.ljust(col_cantidad)}"
        reporte += f"{'Medida'.ljust(col_medida)}\n"
        reporte += "-" * ancho_linea + "\n"
        
        if productos_bajo_stock:
            for producto in productos_bajo_stock:
                reporte += f"{str(producto.codigo).ljust(col_codigo)}"
                reporte += f"{producto.nombre[:28].ljust(col_nombre)}"
                reporte += f"{str(producto.cantidad).ljust(col_cantidad)}"
                reporte += f"{str(producto.stock_minimo).ljust(col_cantidad)}"
                reporte += f"{"Reabastecer" if producto.cantidad <= producto.stock_minimo else "".ljust(col_medida)}\n"
        else:
            reporte += f"{'N/A'.ljust(col_codigo)}"
            reporte += f"{'Sin productos'.ljust(col_nombre)}"
            reporte += f"{'0'.ljust(col_cantidad)}"
            reporte += f"{'0'.ljust(col_cantidad)}"
            reporte += f"{'N/A'.ljust(col_medida)}\n"

        # Sección de productos más vendidos
        reporte += "\n" + "PRODUCTOS MÁS VENDIDOS".center(ancho_linea) + "\n"
        reporte += "=" * ancho_linea + "\n"
        
        reporte += f"{'Código'.ljust(col_codigo)}{'Nombre'.ljust(col_nombre)}"
        reporte += f"{'Precio'.ljust(col_precio)}{'Stock'.ljust(col_cantidad)}"
        reporte += f"{'Vendidos'.ljust(col_ventas)}\n"
        reporte += "-" * ancho_linea + "\n"
        
        if productos_mas_vendidos:
            for producto in productos_mas_vendidos:
                reporte += f"{str(producto.codigo).ljust(col_codigo)}"
                reporte += f"{producto.nombre[:28].ljust(col_nombre)}"
                reporte += f"${str(producto.precio).ljust(col_precio-1)}"
                reporte += f"{str(producto.cantidad).ljust(col_cantidad)}"
                reporte += f"{str(producto.ventas).ljust(col_ventas)}\n"
        else:
            reporte += f"{'N/A'.ljust(col_codigo)}"
            reporte += f"{'Sin productos'.ljust(col_nombre)}"
            reporte += f"${'0'.ljust(col_precio-1)}"
            reporte += f"{'0'.ljust(col_cantidad)}"
            reporte += f"{'0'.ljust(col_ventas)}\n"

        # Sección de productos menos vendidos
        reporte += "\n" + "PRODUCTOS MENOS VENDIDOS".center(ancho_linea) + "\n"
        reporte += "=" * ancho_linea + "\n"
        
        reporte += f"{'Código'.ljust(col_codigo)}{'Nombre'.ljust(col_nombre)}"
        reporte += f"{'Precio'.ljust(col_precio)}{'Stock'.ljust(col_cantidad)}"
        reporte += f"{'Vendidos'.ljust(col_ventas)}\n"
        reporte += "-" * ancho_linea + "\n"
        
        if productos_menos_vendidos:
            for producto in productos_menos_vendidos:
                reporte += f"{str(producto.codigo).ljust(col_codigo)}"
                reporte += f"{producto.nombre[:28].ljust(col_nombre)}"
                reporte += f"${str(producto.precio).ljust(col_precio-1)}"
                reporte += f"{str(producto.cantidad).ljust(col_cantidad)}"
                reporte += f"{str(producto.ventas).ljust(col_ventas)}\n"
        else:
            reporte += f"{'N/A'.ljust(col_codigo)}"
            reporte += f"{'Sin productos'.ljust(col_nombre)}"
            reporte += f"${'0'.ljust(col_precio-1)}"
            reporte += f"{'0'.ljust(col_cantidad)}"
            reporte += f"{'0'.ljust(col_ventas)}\n"

        return reporte

    def mostrar_menu(self):
        while True:
            self.limpiar_pantalla()
            print("""
=== SISTEMA DE INVENTARIO GIFTY ===
1. Agregar producto
2. Actualizar producto
3. Eliminar producto
4. Ver inventario
5. Buscar producto
6. Registrar venta
7. Generar reporte
8. Salir
""")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                while True:
                    codigo_str = input("Ingrese el código del producto (número entero positivo): ")
                    valido, codigo = self.validar_codigo(codigo_str)
                    if valido:
                        break

                while True:
                    nombre = input("Ingrese el nombre del producto: ")
                    if self.validar_nombre(nombre):
                        break

                while True:
                    try:
                        precio = float(input("Ingrese el precio del producto: "))
                        if precio <= 0:
                            print("El precio debe ser mayor que 0.")
                            continue
                        break
                    except ValueError:
                        print("Por favor, ingrese un número válido para el precio.")

                while True:
                    try:
                        cantidad = int(input("Ingrese la cantidad inicial: "))
                        if cantidad < 0:
                            print("La cantidad no puede ser negativa.")
                            continue
                        break
                    except ValueError:
                        print("Por favor, ingrese un número entero para la cantidad.")

                while True:
                    try:
                        stock_minimo_str = input("Ingrese el stock mínimo (Enter para usar 5): ")
                        if not stock_minimo_str:
                            stock_minimo = 5
                            break
                        stock_minimo = int(stock_minimo_str)
                        if stock_minimo <= 0:
                            print("El stock mínimo debe ser mayor que 0.")
                            continue
                        break
                    except ValueError:
                        print("Por favor, ingrese un número entero para el stock mínimo.")

                self.agregar_producto(codigo, nombre, precio, cantidad, stock_minimo)

            elif opcion == "2":
                while True:
                    codigo_str = input("Ingrese el código del producto a actualizar: ")
                    valido, codigo = self.validar_codigo_existente(codigo_str)
                    if valido:
                        producto = self.productos[codigo]
                        print(f"\nInformación actual del producto:")
                        print(f"Nombre: {producto.nombre}")
                        print(f"Precio: ${producto.precio:.2f}")
                        print(f"Cantidad actual: {producto.cantidad}")
                        break

                nombre = input("\nIngrese el nuevo nombre (Enter para mantener): ")
                precio_str = input("Ingrese el nuevo precio (Enter para mantener): ")
                cantidad_str = input("Ingrese la cantidad a agregar (Enter para mantener): ")
                
                precio = None
                if precio_str:
                    try:
                        precio = float(precio_str)
                        if precio <= 0:
                            print("El precio debe ser mayor que 0.")
                            precio = None
                    except ValueError:
                        print("Precio inválido, se mantendrá el valor actual.")

                cantidad = None
                if cantidad_str:
                    try:
                        cantidad = int(cantidad_str)
                        if cantidad < 0:
                            print("La cantidad no puede ser negativa.")
                            cantidad = None
                    except ValueError:
                        print("Cantidad inválida, se mantendrá el valor actual.")

                self.actualizar_producto(codigo, nombre, precio, cantidad)

            elif opcion == "3":
                while True:
                    codigo_str = input("Ingrese el código del producto a eliminar: ")
                    valido, codigo = self.validar_codigo_existente(codigo_str)
                    if valido:
                        break
                self.eliminar_producto(codigo)

            elif opcion == "4":
                print("\n=== Inventario actual ===")
                if not self.productos:
                    print("El inventario no contiene productos actualmente.")
                else:
                    for producto in self.productos.values():
                        print(producto)
                    # Aquí se agrega la alerta de stock bajo después de mostrar el inventario
                    self.mostrar_alerta_stock_bajo()
                
            elif opcion == "5":
                termino = input("Ingrese el nombre del producto: ")
                resultados = self.buscar_producto(termino)
                print("\n=== RESULTADOS DE LA BÚSQUEDA ===")
                if resultados:
                    for producto in resultados:
                        print(producto)
                else:
                    print("No se encontraron productos.")

            elif opcion == "6":
                while True:
                    codigo_str = input("Ingrese el código del producto: ")
                    valido, codigo = self.validar_codigo_existente(codigo_str)
                    if valido:
                        break

                while True:
                    try:
                        cantidad = int(input("Ingrese la cantidad vendida: "))
                        if cantidad <= 0:
                            print("La cantidad debe ser mayor que 0.")
                            continue
                        break
                    except ValueError:
                        print("Por favor, ingrese un número entero para la cantidad.")

                self.registrar_venta(codigo, cantidad)

            elif opcion == "7":
                print(self.generar_reporte())

            elif opcion == "8":
                print("\n¡Gracias por usar el Sistema de Inventario Gifty!")
                break

            else:
                print("\nOpción no válida. Por favor, intente nuevamente.")

            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    sistema = SistemaInventario()
    sistema.mostrar_menu()
