# main.py — Punto de entrada y menú principal
import datetime

from presupuesto.datos    import MOVIMIENTOS_RAW
from presupuesto.logica   import parsear_movimientos
from presupuesto.reporte  import imprimir_reporte, exportar_reporte
from presupuesto.graficos import generar_graficos

def menu(movimientos):
    while True:
        print("\n┌─────────────────────────────────────┐")
        print("│   💰  PRESUPUESTO PERSONAL           │")
        print("├─────────────────────────────────────┤")
        print("│  1. Ver reporte completo             │")
        print("│  2. Ver gráficos                     │")
        print("│  3. Agregar movimiento               │")
        print("│  4. Exportar reporte (.txt)          │")
        print("│  5. Salir                            │")
        print("└─────────────────────────────────────┘")
        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            imprimir_reporte(movimientos)

        elif opcion == "2":
            generar_graficos(movimientos)

        elif opcion == "3":
            print("\n📝  Agregar nuevo movimiento")
            tipo = ""
            while tipo not in ("ingreso", "gasto"):
                tipo = input("  Tipo (ingreso / gasto): ").strip().lower()

            categoria   = input("  Categoría (ej. Alimentación): ").strip().capitalize()
            descripcion = input("  Descripción: ").strip()

            while True:
                try:
                    monto = float(input("  Monto: $").strip().replace(".", "").replace(",", ""))
                    break
                except ValueError:
                    print("  ⚠️  Ingresa un número válido.")

            fecha_str = input("  Fecha (YYYY-MM-DD) [Enter = hoy]: ").strip()
            if not fecha_str:
                fecha_str = datetime.date.today().strftime("%Y-%m-%d")

            try:
                fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                print("  ⚠️  Fecha inválida. Se usará la fecha de hoy.")
                fecha = datetime.datetime.today()

            movimientos.append({
                "fecha":       fecha,
                "mes":         fecha.strftime("%Y-%m"),
                "tipo":        tipo,
                "categoria":   categoria,
                "descripcion": descripcion,
                "monto":       monto,
            })
            print(f"\n  ✅  Movimiento agregado: {tipo.upper()} | {categoria} | ${monto:,.0f}")

        elif opcion == "4":
            exportar_reporte(movimientos)

        elif opcion == "5":
            print("\n  👋  ¡Hasta luego!\n")
            break

        else:
            print("  ⚠️  Opción no válida.")


if __name__ == "__main__":
    movimientos = parsear_movimientos(MOVIMIENTOS_RAW)
    menu(movimientos)