# ==============================================================================
# SISTEMA DE GESTIÓN DE BIBLIOTECA DEL BARRIO
# Autor: Sebastián Ospino Mendoza
# Descripción: Control de libros, usuarios, préstamos y cálculo de multas.
# ==============================================================================
VALOR_MULTA_POR_DIA = 1500


def pedir_texto_no_vacio(mensaje):
    """Solicita un texto al usuario y repite hasta que no esté vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("  [Aviso] Este campo no puede quedar vacío. Intente nuevamente.")


def pedir_entero_valido(mensaje, minimo=0):
    """Solicita un número entero mayor o igual al mínimo usando try/except."""
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
            if numero >= minimo:
                return numero
            else:
                print(f"  [Aviso] El número debe ser mayor o igual a {minimo}.")
        except ValueError:
            print("  [Error] Entrada inválida. Debe escribir un número entero (ej: 1, 5, 10).")


def buscar_libro_por_codigo(codigo, lista_libros):
    """Busca un libro por su código único y devuelve su diccionario o None."""
    for libro in lista_libros:
        if libro["codigo"].lower() == codigo.lower():
            return libro
    return None


def buscar_usuario_por_documento(documento, lista_usuarios):
    """Busca un usuario por su documento y devuelve su diccionario o None."""
    for usuario in lista_usuarios:
        if usuario["documento"] == documento:
            return usuario
    return None


# ==============================================================================
# FUNCIONES PRINCIPALES DE GESTIÓN
# ==============================================================================

def registrar_libro(lista_libros):
    """Registra un libro nuevo en el inventario verificando que el código sea único."""
    print("\n--- 1. REGISTRAR NUEVO LIBRO ---")
    codigo = pedir_texto_no_vacio("Ingrese el código único del libro (ej: L01): ")

    # Verificar que el código no exista previamente
    while buscar_libro_por_codigo(codigo, lista_libros) is not None:
        print(f"  [Error] Ya existe un libro registrado con el código '{codigo}'.")
        codigo = pedir_texto_no_vacio("Ingrese un código diferente para el libro: ")

    titulo = pedir_texto_no_vacio("Ingrese el título del libro: ").title()
    autor = pedir_texto_no_vacio("Ingrese el nombre del autor: ").title()
    cantidad_total = pedir_entero_valido("Ingrese la cantidad de ejemplares disponibles: ", minimo=1)

    nuevo_libro = {
        "codigo": codigo.upper(),
        "titulo": titulo,
        "autor": autor,
        "disponibles": cantidad_total
    }

    lista_libros.append(nuevo_libro)
    print(f"\n  [Éxito] Libro '{titulo}' registrado correctamente con {cantidad_total} ejemplar(es).")


def registrar_usuario(lista_usuarios):
    """Registra un usuario nuevo de la biblioteca validando documento único."""
    print("\n--- 2. REGISTRAR NUEVO USUARIO ---")
    documento = pedir_texto_no_vacio("Ingrese el número de documento del usuario: ")

    # Validar que el documento sea numérico
    while not documento.isdigit():
        print("  [Error] El documento debe contener únicamente números.")
        documento = pedir_texto_no_vacio("Ingrese el número de documento del usuario: ")

    # Verificar que no esté ya registrado
    while buscar_usuario_por_documento(documento, lista_usuarios) is not None:
        print(f"  [Error] El documento '{documento}' ya está registrado en el sistema.")
        documento = pedir_texto_no_vacio("Ingrese otro número de documento: ")

    nombre = pedir_texto_no_vacio("Ingrese el nombre completo del usuario: ").title()
    telefono = pedir_texto_no_vacio("Ingrese el teléfono de contacto: ")

    nuevo_usuario = {
        "documento": documento,
        "nombre": nombre,
        "telefono": telefono
    }

    lista_usuarios.append(nuevo_usuario)
    print(f"\n  [Éxito] Usuario '{nombre}' registrado correctamente.")


def prestar_libro(lista_libros, lista_usuarios, lista_prestamos):
    """Registra el préstamo de un libro a un usuario y descuenta disponibilidad."""
    print("\n--- 3. REALIZAR PRÉSTAMO DE LIBRO ---")

    if len(lista_libros) == 0:
        print("  [Aviso] No hay libros registrados en la biblioteca todavía.")
        return

    if len(lista_usuarios) == 0:
        print("  [Aviso] No hay usuarios registrados. Registre primero un usuario.")
        return

    documento = pedir_texto_no_vacio("Ingrese el documento del usuario que solicita el libro: ")
    usuario = buscar_usuario_por_documento(documento, lista_usuarios)

    if usuario is None:
        print(f"  [Error] No se encontró ningún usuario con el documento '{documento}'.")
        return

    codigo_libro = pedir_texto_no_vacio("Ingrese el código del libro a prestar: ")
    libro = buscar_libro_por_codigo(codigo_libro, lista_libros)

    if libro is None:
        print(f"  [Error] No existe ningún libro con el código '{codigo_libro}'.")
        return

    if libro["disponibles"] <= 0:
        print(f"  [Aviso] Lo sentimos, no hay ejemplares disponibles de '{libro['titulo']}' en este momento.")
        return

    dias_plazo = pedir_entero_valido("¿Por cuántos días se presta el libro? (mínimo 1): ", minimo=1)

    # Descontar un ejemplar disponible
    libro["disponibles"] -= 1

    # Crear el registro del préstamo con un ID consecutivo
    id_prestamo = len(lista_prestamos) + 1
    nuevo_prestamo = {
        "id_prestamo": id_prestamo,
        "documento_usuario": usuario["documento"],
        "nombre_usuario": usuario["nombre"],
        "codigo_libro": libro["codigo"],
        "titulo_libro": libro["titulo"],
        "dias_plazo": dias_plazo,
        "devuelto": False,
        "multa_pagada": 0
    }

    lista_prestamos.append(nuevo_prestamo)
    print("\n  [Éxito] Préstamo registrado correctamente:")
    print(f"  - N° de Préstamo : {id_prestamo}")
    print(f"  - Usuario        : {usuario['nombre']}")
    print(f"  - Libro          : {libro['titulo']}")
    print(f"  - Plazo máximo   : {dias_plazo} día(s)")


def devolver_libro_y_calcular_multa(lista_libros, lista_prestamos):
    """Procesa la devolución de un libro, calcula multa por retraso y repone el stock."""
    print("\n--- 4. DEVOLVER LIBRO Y CALCULAR MULTA ---")

    # Filtrar préstamos activos (no devueltos)
    prestamos_activos = [p for p in lista_prestamos if not p["devuelto"]]

    if len(prestamos_activos) == 0:
        print("  [Aviso] No hay préstamos pendientes por devolver en este momento.")
        return

    print("\nPréstamos activos actuales:")
    for p in prestamos_activos:
        print(f"  ID: {p['id_prestamo']} | Usuario: {p['nombre_usuario']} ({p['documento_usuario']}) | Libro: {p['titulo_libro']} (Plazo: {p['dias_plazo']} días)")

    id_buscar = pedir_entero_valido("\nIngrese el ID del préstamo que desea devolver: ", minimo=1)

    prestamo_encontrado = None
    for p in prestamos_activos:
        if p["id_prestamo"] == id_buscar:
            prestamo_encontrado = p
            break

    if prestamo_encontrado is None:
        print(f"  [Error] No se encontró un préstamo activo con el ID {id_buscar}.")
        return

    dias_reales = pedir_entero_valido("¿Cuántos días en total tuvo el usuario el libro?: ", minimo=0)

    # Cálculo de retraso y multa
    dias_retraso = dias_reales - prestamo_encontrado["dias_plazo"]
    multa = 0

    if dias_retraso > 0:
        multa = dias_retraso * VALOR_MULTA_POR_DIA
        print(f"\n  [Alerta de Retraso] El libro se entregó con {dias_retraso} día(s) de retraso.")
        print(f"  [Multa a Pagar] Valor por día: ${VALOR_MULTA_POR_DIA} -> Total multa: ${multa}")
    else:
        print("\n  [A tiempo] El libro fue devuelto dentro del plazo establecido. No genera multa.")

    # Actualizar estado del préstamo y devolver el ejemplar al inventario
    prestamo_encontrado["devuelto"] = True
    prestamo_encontrado["multa_pagada"] = multa

    libro = buscar_libro_por_codigo(prestamo_encontrado["codigo_libro"], lista_libros)
    if libro is not None:
        libro["disponibles"] += 1

    print(f"  [Éxito] Devolución completada. El libro '{prestamo_encontrado['titulo_libro']}' vuelve a estar disponible.")


def consultar_estado_biblioteca(lista_libros, lista_usuarios, lista_prestamos):
    """Muestra reportes completos de libros, usuarios y préstamos activos."""
    print("\n--- 5. CONSULTAR INVENTARIO Y PRÉSTAMOS ---")
    print("1) Ver catálogo de libros")
    print("2) Ver usuarios registrados")
    print("3) Ver historial de préstamos")

    opcion_consulta = input("Seleccione una opción (1-3): ").strip()

    if opcion_consulta == "1":
        if len(lista_libros) == 0:
            print("  [Aviso] No hay libros registrados.")
        else:
            print("\n" + "=" * 75)
            print(f"{'CÓDIGO':<10} | {'TÍTULO':<30} | {'AUTOR':<20} | {'DISP.':<6}")
            print("-" * 75)
            for libro in lista_libros:
                print(f"{libro['codigo']:<10} | {libro['titulo']:<30} | {libro['autor']:<20} | {libro['disponibles']:<6}")
            print("=" * 75)

    elif opcion_consulta == "2":
        if len(lista_usuarios) == 0:
            print("  [Aviso] No hay usuarios registrados.")
        else:
            print("\n" + "=" * 65)
            print(f"{'DOCUMENTO':<15} | {'NOMBRE COMPLETO':<30} | {'TELÉFONO':<15}")
            print("-" * 65)
            for u in lista_usuarios:
                print(f"{u['documento']:<15} | {u['nombre']:<30} | {u['telefono']:<15}")
            print("=" * 65)

    elif opcion_consulta == "3":
        if len(lista_prestamos) == 0:
            print("  [Aviso] No se han realizado préstamos todavía.")
        else:
            print("\n" + "=" * 85)
            print(f"{'ID':<5} | {'USUARIO':<22} | {'LIBRO':<25} | {'ESTADO':<12} | {'MULTA':<10}")
            print("-" * 85)
            for p in lista_prestamos:
                estado = "Devuelto" if p["devuelto"] else "Prestado"
                print(f"{p['id_prestamo']:<5} | {p['nombre_usuario']:<22} | {p['titulo_libro']:<25} | {estado:<12} | ${p['multa_pagada']:<9}")
            print("=" * 85)
    else:
        print("  [Error] Opción de consulta no válida.")


# ==============================================================================
# MENÚ PRINCIPAL DEL PROGRAMA
# ==============================================================================

def iniciar_sistema():
    """Función principal que mantiene el programa en ejecución constante."""
    libros = []
    usuarios = []
    prestamos = []

    while True:
        print("\n==================================================")
        print("       SISTEMA DE GESTIÓN - BIBLIOTECA BARRIO     ")
        print("==================================================")
        print("1. Registrar libro")
        print("2. Registrar usuario")
        print("3. Prestar libro")
        print("4. Devolver libro y calcular multa")
        print("5. Consultar libros, usuarios y préstamos")
        print("6. Salir del sistema")
        print("==================================================")

        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            registrar_libro(libros)
        elif opcion == "2":
            registrar_usuario(usuarios)
        elif opcion == "3":
            prestar_libro(libros, usuarios, prestamos)
        elif opcion == "4":
            devolver_libro_y_calcular_multa(libros, prestamos)
        elif opcion == "5":
            consultar_estado_biblioteca(libros, usuarios, prestamos)
        elif opcion == "6":
            print("\nGracias por usar el Sistema de Gestión de la Biblioteca. ¡Hasta pronto!")
            break
        else:
            print("\n  [Error] Opción inválida. Por favor ingrese un número entre 1 y 6.")


# Punto de entrada seguro del programa
if __name__ == "__main__":
    try:
        iniciar_sistema()
    except KeyboardInterrupt:
        print("\n\n  [Aviso] Programa cerrado manualmente por el usuario.")
    except Exception as error_inesperado:
        print(f"\n  [Error controlado] Ocurrió un problema inesperado: {error_inesperado}")