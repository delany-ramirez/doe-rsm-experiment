"""Interfaz de línea de comandos del proceso experimental."""

from __future__ import annotations

import sys
from pathlib import Path

import click

if sys.stdout.encoding is not None and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from experiment.runner import (
    X1_RANGE,
    X2_RANGE,
    append_result,
    load_history,
    next_corrida_number,
    run_experiment,
    to_coded,
    to_real,
    validate_ranges,
)

RESULTADOS_CSV = Path("resultados.csv")


@click.command()
@click.option("--x1", type=float, default=None, help="Factor x1 (learning_rate).")
@click.option("--x2", type=float, default=None, help="Factor x2 (max_depth).")
@click.option("--semilla", type=int, default=42, show_default=True, help="Semilla aleatoria de la corrida.")
@click.option(
    "--codificado",
    is_flag=True,
    default=False,
    help="Interpreta --x1 y --x2 en escala codificada [-1, +1] en lugar de unidades naturales.",
)
@click.option("--historial", is_flag=True, default=False, help="Muestra todas las corridas acumuladas.")
def main(x1: float | None, x2: float | None, semilla: int, codificado: bool, historial: bool) -> None:
    if historial:
        _mostrar_historial()
        return

    if x1 is None or x2 is None:
        click.echo("Error: debes especificar --x1 y --x2 (o usar --historial).")
        sys.exit(1)

    if codificado:
        x1_real = to_real(x1, *X1_RANGE)
        x2_real = to_real(x2, *X2_RANGE)
    else:
        x1_real = x1
        x2_real = x2

    error = validate_ranges(x1_real, x2_real)
    if error is not None:
        click.echo(f"Error: {error}")
        click.echo("La corrida no fue registrada.")
        sys.exit(1)

    x2_real_int = round(x2_real)
    x1_cod = to_coded(x1_real, *X1_RANGE)
    x2_cod = to_coded(x2_real_int, *X2_RANGE)

    y = run_experiment(x1_real, x2_real_int, semilla)

    corrida = next_corrida_number(RESULTADOS_CSV)
    append_result(
        RESULTADOS_CSV,
        {
            "corrida": corrida,
            "x1_real": x1_real,
            "x2_real": x2_real_int,
            "x1_cod": x1_cod,
            "x2_cod": x2_cod,
            "semilla": semilla,
            "y": y,
        },
    )

    click.echo(f"Corrida #{corrida}")
    click.echo(f"x1 (learning_rate) = {x1_real:.4f}  (codificado: {x1_cod:+.2f})")
    click.echo(f"x2 (max_depth)     = {x2_real_int}       (codificado: {x2_cod:+.2f})")
    click.echo(f"semilla            = {semilla}")
    click.echo(f"y (R²)             = {y:.4f}")


def _mostrar_historial() -> None:
    df = load_history(RESULTADOS_CSV)
    if df is None or df.empty:
        click.echo("Todavía no hay corridas registradas.")
        return
    click.echo(df.to_string(index=False))


if __name__ == "__main__":
    main()
