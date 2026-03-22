# reporte.py — Impresión y exportación del reporte
from presupuesto.logica import resumen_mensual, gastos_por_categoria


def imprimir_reporte(movimientos):
    resumen    = resumen_mensual(movimientos)
    categorias = gastos_por_categoria(movimientos)

    separador = "═" * 54
    sep_fino  = "─" * 54

    print(f"\n{separador}")
    print("  💰  PRESUPUESTO PERSONAL — REPORTE GENERAL")
    print(separador)

    # ── Resumen mensual ──────────────────────────────────
    print("\n📅  RESUMEN MENSUAL\n")
    print(f"  {'Mes':<12} {'Ingresos':>14} {'Gastos':>14} {'Balance':>14}")
    print(f"  {sep_fino}")

    total_ingresos_global = 0
    total_gastos_global   = 0

    for mes, datos in resumen.items():
        ingresos = datos["ingresos"]
        gastos   = datos["gastos"]
        balance  = ingresos - gastos
        total_ingresos_global += ingresos
        total_gastos_global   += gastos

        signo = "✅" if balance >= 0 else "❌"
        print(
            f"  {mes:<12} "
            f"${ingresos:>12,.0f} "
            f"${gastos:>12,.0f} "
            f"{signo} ${balance:>10,.0f}"
        )

    balance_global = total_ingresos_global - total_gastos_global
    signo_global   = "✅" if balance_global >= 0 else "❌"

    print(f"  {sep_fino}")
    print(
        f"  {'TOTAL':<12} "
        f"${total_ingresos_global:>12,.0f} "
        f"${total_gastos_global:>12,.0f} "
        f"{signo_global} ${balance_global:>10,.0f}"
    )

    # ── Desglose por categoría ───────────────────────────
    print(f"\n\n📂  GASTOS POR CATEGORÍA\n")
    print(f"  {'Categoría':<22} {'Total':>14}  {'%':>6}")
    print(f"  {sep_fino}")

    for cat, monto in categorias.items():
        porcentaje = (monto / total_gastos_global * 100) if total_gastos_global else 0
        barra = "█" * int(porcentaje / 5)
        print(f"  {cat:<22} ${monto:>12,.0f}  {porcentaje:>5.1f}%  {barra}")

    # ── Detalle de movimientos ───────────────────────────
    print(f"\n\n📋  DETALLE DE MOVIMIENTOS\n")
    print(f"  {'Fecha':<12} {'Tipo':<8} {'Categoría':<18} {'Descripción':<28} {'Monto':>14}")
    print(f"  {sep_fino}")

    for m in sorted(movimientos, key=lambda x: x["fecha"]):
        tipo_icon = "⬆️ " if m["tipo"] == "ingreso" else "⬇️ "
        signo     = "+" if m["tipo"] == "ingreso" else "-"
        print(
            f"  {m['fecha'].strftime('%Y-%m-%d'):<12} "
            f"{tipo_icon}{m['tipo']:<6} "
            f"{m['categoria']:<18} "
            f"{m['descripcion']:<28} "
            f"{signo}${m['monto']:>11,.0f}"
        )

    print(f"\n{separador}\n")


def exportar_reporte(movimientos, ruta="reporte_presupuesto.txt"):
    import io, sys
    buffer = io.StringIO()
    sys.stdout = buffer
    imprimir_reporte(movimientos)
    sys.stdout = sys.__stdout__
    contenido = buffer.getvalue()

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"📄  Reporte exportado: {ruta}")