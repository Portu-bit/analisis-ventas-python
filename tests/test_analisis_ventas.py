import pandas as pd
import pytest

from analisis_ventas import analyze_sales, load_sales_data


def test_load_sales_data_parses_decimal_comma_and_normalizes_products(tmp_path):
    csv_file = tmp_path / "ventas.csv"
    csv_file.write_text(
        "producto,cantidad,precio\nlaptop,2,800\nTeclado,3,3,50\n",
        encoding="utf-8",
    )
    # Quoted decimal comma is a single CSV field.
    csv_file.write_text(
        'producto,cantidad,precio\nlaptop,2,800\nTeclado,3,"3,50"\n',
        encoding="utf-8",
    )
    df = load_sales_data(csv_file)
    assert df.loc[0, "producto"] == "Laptop"
    assert df.loc[1, "precio"] == 3.5


def test_analysis_returns_correct_totals_for_repository_dataset():
    from pathlib import Path
    df = load_sales_data(Path(__file__).with_name("..") / "ventas.csv")
    _, by_product, summary = analyze_sales(df)
    assert summary["ingresos_totales"] == 1915.9
    assert summary["producto_mas_vendido"] == "Mouse"
    assert summary["unidades_vendidas"] == 13
    assert by_product["Mouse"] == 7


@pytest.mark.parametrize(
    "csv_text",
    [
        "producto,cantidad,precio\nMouse,0,20\n",
        "producto,cantidad,precio\nMouse,2,-1\n",
        "producto,cantidad,precio\nMouse,abc,20\n",
        "producto,cantidad,precio\n,2,20\n",
    ],
)
def test_load_rejects_invalid_rows(tmp_path, csv_text):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(csv_text, encoding="utf-8")
    with pytest.raises(ValueError):
        load_sales_data(csv_file)


def test_analyze_rejects_empty_dataframe():
    with pytest.raises(ValueError):
        analyze_sales(pd.DataFrame(columns=["producto", "cantidad", "precio"]))
