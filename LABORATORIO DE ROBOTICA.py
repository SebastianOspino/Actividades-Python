
def validar_id_unico(id_buscar, inventario):
    """Verifica si el ID ya existe en el inventario."""
    for componente in inventario:
        if componente["id"] == id_buscar:
            return True
    return False


def registrar_componente(inventario):
    """Registra un nuevo componente en el inventario validando ID único."""
    print("\n--- 1. REGISTRAR NUEVO COMPONENTE ---")
    comp_id = input("Ingrese el ID único del componente: ").strip()
    
    while validar_id_unico(comp_id, inventario):
        print(f"  ❌ ERROR: El ID '{comp_id}' ya existe. Ingrese un ID diferente.")
        comp_id = input("  Ingrese el ID único del componente: ").strip()
        
    nombre = input("Ingrese el nombre del componente: ").strip().capitalize()
    
    print("\nCategorías sugeridas: Sensores, Actuadores, Microcontroladores, Pantallas, Motores")
    categoria = input("Ingrese la categoría: ").strip().capitalize()
    
    # Validación de stock (entero >= 0)
    stock = int(input("Ingrese la cantidad inicial en stock: "))
    while stock < 0:
        print("  ❌ ERROR: El stock no puede ser negativo.")
        stock = int(input("  Ingrese la cantidad inicial en stock: "))
        
    # Validación de precio unitario (flotante > 0)
    precio = float(input("Ingrese el precio unitario: "))
    while precio <= 0:
        print("  ❌ ERROR: El precio debe ser mayor a 0.")
        precio = float(input("  Ingrese el precio unitario: "))
        
    nuevo_componente = {
        "id": comp_id,
        "nombre": nombre,
        "categoria": categoria,
        "stock": stock,
        "precio_unitario": precio
    }
    
    inventario.append(nuevo_componente)
    print(f"\n  ✅ Componente '{nombre}' (ID: {comp_id}) registrado con éxito.")


def consultar_y_filtrar(inventario):
    """Muestra el inventario completo o filtrado por categoría."""
    print("\n--- 2. CONSULTAR Y FILTRAR INVENTARIO ---")
    if len(inventario) == 0:
        print("  ⚠️ El inventario está vacío.")
        return
        
    print("1) Mostrar TODOS los componentes")
    print("2) Filtrar por categoría")
    sub_opcion = input("Seleccione una opción (1-2): ").strip()
    
    lista_mostrar = []
    
    if sub_opcion == "1":
        lista_mostrar = inventario
    elif sub_opcion == "2":
        cat_buscar = input("Ingrese la categoría a buscar: ").strip().capitalize()
        for comp in inventario:
            if comp["categoria"] == cat_buscar:
                lista_mostrar.append(comp)
    else:
        print("  ❌ Opción no válida.")
        return

    if len(lista_mostrar) == 0:
        print("  ⚠️ No se encontraron componentes para esa consulta.")
    else:
        print("\n" + "=" * 75)
        print(f"{'ID':<10} | {'Nombre':<20} | {'Categoría':<18} | {'Stock':<8} | {'Precio ($)':<10}")
        print("-" * 75)
        for comp in lista_mostrar:
            print(f"{comp['id']:<10} | {comp['nombre']:<20} | {comp['categoria']:<18} | {comp['stock']:<8} | ${comp['precio_unitario']:<9.2f}")
        print("=" * 75)


def actualizar_stock(inventario):
    """Busca un componente por su ID y suma o resta unidades del stock."""
    print("\n--- 3. ACTUALIZAR STOCK DE COMPONENTE ---")
    if len(inventario) == 0:
        print("  ⚠️ El inventario está vacío.")
        return
        
    id_buscar = input("Ingrese el ID del componente a actualizar: ").strip()
    
    componente_encontrado = None
    for comp in inventario:
        if comp["id"] == id_buscar:
            componente_encontrado = comp
            break
            
    if componente_encontrado is None:
        print(f"  ❌ No se encontró ningún componente con el ID '{id_buscar}'.")
    else:
        print(f"\nComponente: {componente_encontrado['nombre']} | Stock actual: {componente_encontrado['stock']}")
        print("1) Sumar stock")
        print("2) Restar stock")
        tipo_operacion = input("Seleccione una opción (1-2): ").strip()
        
        if tipo_operacion == "1":
            cantidad = int(input("Cantidad a agregar: "))
            while cantidad <= 0:
                print("  ❌ Debe ingresar una cantidad mayor a 0.")
                cantidad = int(input("Cantidad a agregar: "))
            componente_encontrado["stock"] += cantidad
            print(f"  ✅ Stock actualizado. Nuevo stock: {componente_encontrado['stock']}")
            
        elif tipo_operacion == "2":
            cantidad = int(input("Cantidad a retirar: "))
            while cantidad <= 0:
                print("  ❌ Debe ingresar una cantidad mayor a 0.")
                cantidad = int(input("Cantidad a retirar: "))
                
            if cantidad > componente_encontrado["stock"]:
                print(f"  ❌ ERROR: Stock insuficiente. Solo hay {componente_encontrado['stock']} unidades disponibles.")
            else:
                componente_encontrado["stock"] -= cantidad
                print(f"  ✅ Stock actualizado. Nuevo stock: {componente_encontrado['stock']}")
        else:
            print("  ❌ Opción inválida.")


def menu_principal():
    """Bucle principal del programa."""
    inventario = []
    opcion = ""
    
    while opcion != "4":
        print("\n==================================================")
        print("  INVENTARIO LABORATORIO DE ROBÓTICA - MENÚ  ")
        print("==================================================")
        print("1) Registrar componente")
        print("2) Consultar y filtrar componentes")
        print("3) Actualizar stock (Entrada/Salida)")
        print("4) Salir")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            registrar_componente(inventario)
        elif opcion == "2":
            consultar_y_filtrar(inventario)
        elif opcion == "3":
            actualizar_stock(inventario)
        elif opcion == "4":
            print("\n  👋 Saliendo del sistema de inventario. ¡Éxitos!")
        else:
            print("  ❌ Opción no válida. Por favor elija un número del 1 al 4.")


if __name__ == "__main__":
    menu_principal()