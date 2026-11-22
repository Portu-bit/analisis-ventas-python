from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_CSV = Path(__file__).with_name("ventas.csv")
REQUIRED_COLUMNS = {"producto", "cantidad", "precio"}


def load_sales_data(csv_path=DEFAULT_CSV):
    """Load and validate the sales CSV, accepting decimal commas or points."""
    df = pd.read_csv(csv_path)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(sorted(missing_columns))}")

    df = df.copy()
    df["producto"] = df["producto"].astype("string").str.strip().str.title()
    if df["producto"].isna().any() or df["producto"].eq("").any():
        raise ValueError("Los nombres de producto no pueden estar vacíos.")

    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    normalized_prices = df["precio"].astype("string").str.replace(",", ".", regex=False)
    df["precio"] = pd.to_numeric(normalized_prices, errors="coerce")

    if df[["cantidad", "precio"]].isna().any().any():
        raise ValueError("Cantidad y precio deben contener valores numéricos.")
    if (df["cantidad"] <= 0).any() or (df["precio"] <= 0).any():
        raise ValueError("Cantidad y precio deben ser mayores que cero.")
    if (df["cantidad"] % 1 != 0).any():
        raise ValueError("La cantidad debe ser un número entero.")

    df["cantidad"] = df["cantidad"].astype(int)
    return df


def analyze_sales(df):
    """Return the enriched data, units sold per product, and key metrics."""
    if df.empty:
        raise ValueError("No hay registros de ventas para analizar.")
    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError("El DataFrame debe incluir producto, cantidad y precio.")

    analyzed = df.copy()
    analyzed["ingresos"] = analyzed["cantidad"] * analyzed["precio"]
    sales_by_product = (
        analyzed.groupby("producto")["cantidad"]
        .sum()
        .sort_values(ascending=False, kind="stable")
    )
    summary = {
        "ingresos_totales": round(float(analyzed["ingresos"].sum()), 2),
        "producto_mas_vendido": str(sales_by_product.idxmax()),
        "unidades_vendidas": int(analyzed["cantidad"].sum()),
    }
    return analyzed, sales_by_product, summary


def plot_sales_by_product(sales_by_product):
    """Create a bar chart and return its figure and axes."""
    if sales_by_product.empty:
        raise ValueError("No hay ventas para graficar.")
    ax = sales_by_product.plot(kind="bar")
    ax.set_title("Unidades vendidas por producto")
    ax.set_xlabel("Producto")
    ax.set_ylabel("Unidades vendidas")
    fig = ax.get_figure()
    fig.tight_layout()
    return fig, ax


def main():
    sales = load_sales_data()
    analyzed, sales_by_product, summary = analyze_sales(sales)
    print(f"Ingresos totales: {summary['ingresos_totales']:.2f}")
    print(f"Producto más vendido: {summary['producto_mas_vendido']}")
    print(f"Unidades vendidas: {summary['unidades_vendidas']}")
    print("\nUnidades vendidas por producto:")
    print(sales_by_product)
    plot_sales_by_product(sales_by_product)
    plt.show()


if __name__ == "__main__":
    main()
