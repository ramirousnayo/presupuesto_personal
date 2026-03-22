# logica.py — Funciones de cálculo y procesamiento
import datetime
from collections import defaultdict


def parsear_movimientos(raw):
    """Convierte la lista cruda de tuplas en lista de diccionarios."""
    movimientos = []
    for fecha_str, tipo, categoria, descripcion, monto in raw:
        fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
        movimientos.append({
            "fecha":       fecha,
            "mes":         fecha.strftime("%Y-%m"),
            "tipo":        tipo,
            "categoria":   categoria,
            "descripcion": descripcion,
            "monto":       monto,
        })
    return movimientos


def resumen_mensual(movimientos):
    """Agrupa ingresos y gastos por mes."""
    meses = defaultdict(lambda: {"ingresos": 0, "gastos": 0})
    for m in movimientos:
        if m["tipo"] == "ingreso":
            meses[m["mes"]]["ingresos"] += m["monto"]
        else:
            meses[m["mes"]]["gastos"] += m["monto"]
    return dict(sorted(meses.items()))


def gastos_por_categoria(movimientos):
    """Suma los gastos agrupados por categoría."""
    cats = defaultdict(int)
    for m in movimientos:
        if m["tipo"] == "gasto":
            cats[m["categoria"]] += m["monto"]
    return dict(sorted(cats.items(), key=lambda x: x[1], reverse=True))