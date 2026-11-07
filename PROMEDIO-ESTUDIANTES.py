def solicitar_nota_valida(nombre_estudiante):
    nota = float(input(f"Ingrese la nota de {nombre_estudiante} (1.0 a 5.0): "))
    while nota < 1.0 or nota > 5.0:
        print("  ERROR: La nota debe ser no menor a 1.0 y no mayor que 5.0.")
        nota = float(input(f"  Ingrese nuevamente la nota de {nombre_estudiante}: "))
    return nota


def registrar_estudiante(lista_estudiantes):
    print("\n--- 1. REGISTRAR ESTUDIANTE ---")
    nombre = input("Ingrese el nombre del estudiante: ").strip().capitalize()
    nota = solicitar_nota_valida(nombre)
    
    estudiante = {
        "nombre": nombre,
        "nota": nota
    }
    
    lista_estudiantes.append(estudiante)
    print(f"  ¡Estudiante '{nombre}' con nota {nota} registrado con éxito!")


def mostrar_estudiantes(lista_estudiantes):
    print("\n--- 2. MOSTRAR ESTUDIANTES ---")
    if len(lista_estudiantes) == 0:
        print("  No hay estudiantes registrados en el sistema.")
    else:
        print(f"{'No.':<5} | {'Nombre':<20} | {'Nota':<5} | {'Estado'}")
        print("-" * 50)
        for i, est in enumerate(lista_estudiantes, start=1):
            estado = "Aprobado" if est["nota"] >= 3.0 else "Reprobado"
            print(f"{i:<5} | {est['nombre']:<20} | {est['nota']:<5.1f} | {estado}")


def calcular_estadisticas(lista_estudiantes):
    print("\n--- 3. ESTADÍSTICAS DE ESTUDIANTES ---")
    if len(lista_estudiantes) == 0:
        print("  No hay suficientes datos para generar estadísticas.")
    else:
        notas = [est["nota"] for est in lista_estudiantes]
        
        promedio = sum(notas) / len(notas)
        nota_maxima = max(notas)
        nota_minima = min(notas)
        
        print(f"  • Total de estudiantes : {len(lista_estudiantes)}")
        print(f"  • Promedio general     : {promedio:.2f}")
        print(f"  • Nota más alta        : {nota_maxima:.1f}")
        print(f"  • Nota más baja        : {nota_minima:.1f}")


def programa_principal():
    estudiantes = []
    opcion = 0
    
    while opcion != 4:
        print("\n==========================================")
        print("     MENÚ DE GESTIÓN DE ESTUDIANTES      ")
        print("==========================================")
        print("1) Registrar estudiante y nota")
        print("2) Mostrar estudiantes")
        print("3) Estadísticas de estudiantes")
        print("4) Salir")
        
        try:
            opcion = int(input("Seleccione una opción (1-4): "))
            
            if opcion == 1:
                registrar_estudiante(estudiantes)
            elif opcion == 2:
                mostrar_estudiantes(estudiantes)
            elif opcion == 3:
                calcular_estadisticas(estudiantes)
            elif opcion == 4:
                print("\n  Saliendo del programa. ¡Muchos éxitos!")
            else:
                print("  Opción fuera de rango. Por favor elija del 1 al 4.")
        except ValueError:
            print("  Entrada inválida. Debe ingresar un número entero.")


if __name__ == "__main__":
    programa_principal()