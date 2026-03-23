# 💰 Presupuesto Personal

Script en Python para registrar y visualizar ingresos y gastos personales, con reporte mensual y gráficos.

## Funcionalidades

- Registro de ingresos y gastos con fecha, categoría y descripción
- Resumen mensual con balance
- Desglose de gastos por categoría
- Gráficos: barras (ingresos vs gastos), línea (balance mensual) y torta (distribución de gastos)
- Exportación de reporte en `.txt`

## Estructura del proyecto

```
presupuesto_personal/
├── presupuesto/
│   ├── __init__.py
│   ├── datos.py       # Lista de movimientos
│   ├── logica.py      # Funciones de cálculo
│   ├── reporte.py     # Impresión y exportación
│   └── graficos.py    # Gráficos con matplotlib
├── main.py            # Menú y punto de entrada
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/ramirousnayo/presupuesto_personal.git
cd presupuesto_personal

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
python3 main.py
```

## Tecnologías

- Python 3
- matplotlib