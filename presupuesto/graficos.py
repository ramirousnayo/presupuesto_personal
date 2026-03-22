# graficos.py — Generación de gráficos con matplotlib
import datetime
from presupuesto.logica import resumen_mensual, gastos_por_categoria

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False


def generar_graficos(movimientos):
    if not GRAFICOS_DISPONIBLES:
        print("⚠️  matplotlib no está instalado. Ejecutá: pip install matplotlib")
        return

    resumen    = resumen_mensual(movimientos)
    categorias = gastos_por_categoria(movimientos)

    meses        = list(resumen.keys())
    ingresos     = [resumen[m]["ingresos"] for m in meses]
    gastos       = [resumen[m]["gastos"]   for m in meses]
    balances     = [i - g for i, g in zip(ingresos, gastos)]
    meses_labels = [datetime.datetime.strptime(m, "%Y-%m").strftime("%b %Y") for m in meses]

    COLOR_INGRESO = "#2ecc71"
    COLOR_GASTO   = "#e74c3c"
    COLOR_BALANCE = "#3498db"
    COLOR_BG      = "#1a1a2e"
    COLOR_PANEL   = "#16213e"
    COLOR_TEXT    = "#ecf0f1"
    COLORES_CATS  = ["#e74c3c","#e67e22","#f1c40f","#2ecc71",
                     "#1abc9c","#3498db","#9b59b6","#e91e63"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    fig.patch.set_facecolor(COLOR_BG)
    fig.suptitle("💰 Presupuesto Personal — Dashboard", fontsize=16,
                 color=COLOR_TEXT, fontweight="bold", y=1.01)

    x     = range(len(meses))
    ancho = 0.35

    # ── Barras: Ingresos vs Gastos ────────────────────────
    ax1 = axes[0]
    ax1.set_facecolor(COLOR_PANEL)
    bars_i = ax1.bar([i - ancho/2 for i in x], ingresos, ancho,
                     label="Ingresos", color=COLOR_INGRESO, alpha=0.85)
    bars_g = ax1.bar([i + ancho/2 for i in x], gastos, ancho,
                     label="Gastos",   color=COLOR_GASTO,   alpha=0.85)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(meses_labels, color=COLOR_TEXT, fontsize=9)
    ax1.tick_params(colors=COLOR_TEXT)
    ax1.set_title("Ingresos vs Gastos", color=COLOR_TEXT, fontweight="bold")
    ax1.set_ylabel("Monto ($)", color=COLOR_TEXT)
    ax1.legend(facecolor=COLOR_PANEL, labelcolor=COLOR_TEXT)
    ax1.grid(axis="y", alpha=0.2, color=COLOR_TEXT)
    for spine in ax1.spines.values():
        spine.set_edgecolor("#2c3e50")
    for bar in list(bars_i) + list(bars_g):
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 5000,
                 f"${h/1e6:.2f}M" if h >= 1_000_000 else f"${h/1000:.0f}k",
                 ha="center", va="bottom", fontsize=7, color=COLOR_TEXT)

    # ── Línea: Balance mensual ────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor(COLOR_PANEL)
    ax2.plot(meses_labels, balances, marker="o", color=COLOR_BALANCE,
             linewidth=2.5, markersize=8)
    ax2.fill_between(meses_labels, balances, alpha=0.15, color=COLOR_BALANCE)
    ax2.axhline(0, color=COLOR_GASTO, linestyle="--", alpha=0.5, linewidth=1)
    ax2.set_title("Balance Mensual", color=COLOR_TEXT, fontweight="bold")
    ax2.set_ylabel("Balance ($)", color=COLOR_TEXT)
    ax2.tick_params(colors=COLOR_TEXT)
    ax2.grid(alpha=0.2, color=COLOR_TEXT)
    for spine in ax2.spines.values():
        spine.set_edgecolor("#2c3e50")
    for mes, bal in zip(meses_labels, balances):
        color = COLOR_INGRESO if bal >= 0 else COLOR_GASTO
        ax2.annotate(f"${bal/1000:.0f}k", (mes, bal),
                     textcoords="offset points", xytext=(0, 10),
                     ha="center", fontsize=8, color=color, fontweight="bold")

    # ── Torta donut: Gastos por categoría ────────────────
    ax3 = axes[2]
    ax3.set_facecolor(COLOR_PANEL)
    labels  = list(categorias.keys())
    valores = list(categorias.values())
    colores_slice = COLORES_CATS[:len(labels)]
    wedges, texts, autotexts = ax3.pie(
        valores, labels=None, autopct="%1.1f%%",
        colors=colores_slice, startangle=140,
        pctdistance=0.75, wedgeprops=dict(width=0.55)
    )
    for autotext in autotexts:
        autotext.set_color(COLOR_TEXT)
        autotext.set_fontsize(8)
    parches = [mpatches.Patch(color=colores_slice[i], label=labels[i])
               for i in range(len(labels))]
    ax3.legend(handles=parches, loc="lower center", bbox_to_anchor=(0.5, -0.18),
               ncol=2, fontsize=8, facecolor=COLOR_PANEL, labelcolor=COLOR_TEXT,
               framealpha=0.5)
    ax3.set_title("Distribución de Gastos", color=COLOR_TEXT, fontweight="bold")

    plt.tight_layout()
    ruta_img = "presupuesto_graficos.png"
    plt.savefig(ruta_img, dpi=150, bbox_inches="tight", facecolor=COLOR_BG)
    print(f"📊  Gráfico guardado: {ruta_img}")
    plt.show()