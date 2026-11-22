# Análisis de ventas con Python

Proyecto de análisis exploratorio de datos con Python, Pandas y Matplotlib. Lee un CSV de ventas, valida sus datos, calcula ingresos y unidades vendidas por producto y genera una gráfica.

## Resultados del conjunto de datos incluido

- Ingresos totales: **1915.90**
- Producto más vendido: **Mouse** (7 unidades)
- Unidades vendidas: **13**

## Tecnologías

- Python 3.11+
- Pandas
- Matplotlib
- Jupyter Notebook
- Pytest

## Estructura

- `ventas.csv`: datos de ejemplo.
- `analisis_ventas.py`: carga, validación, cálculos y gráfica reutilizables.
- `Analisis_ventas.ipynb`: notebook reproducible que utiliza el módulo.
- `tests/`: pruebas automatizadas.

## Instalación

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecutar el análisis

Como script:

```bash
python analisis_ventas.py
```

Como notebook:

```bash
jupyter notebook Analisis_ventas.ipynb
```

El análisis acepta precios con punto decimal y también valores con coma decimal, y normaliza los nombres de producto para evitar duplicados como `laptop` y `Laptop`.

## Ejecutar pruebas

```bash
python -m pytest -q
```
