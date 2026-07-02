# Proceso experimental — Ejercicio de RSM

Esta herramienta simula un **proceso experimental real**: tú fijas los valores de
dos factores controlables, lanzas una corrida y observas la respuesta del
sistema. No se documenta ni se revela qué ocurre "dentro" del proceso — igual
que en un laboratorio real, donde regulas variables de operación pero no
conoces de antemano la ecuación de la superficie de respuesta.

Con las corridas que vayas acumulando construirás, más adelante, el análisis
de superficie de respuesta (RSM) de tu curso de DOE.

## 1. Instalación

```bash
uv sync
```

## 2. Cómo ejecutar una corrida

```bash
# Corrida en unidades naturales (semilla por defecto 42)
uv run corrida --x1 0.05 --x2 6

# Corrida con una semilla distinta
uv run corrida --x1 0.05 --x2 6 --semilla 7

# Corrida en escala codificada [-1, +1]
uv run corrida --x1 -0.67 --x2 0.0 --codificado

# Ver todas las corridas acumuladas
uv run corrida --historial
```

Cada corrida imprime algo como:

```
Corrida #7
x1 (learning_rate) = 0.0500  (codificado: -0.67)
x2 (max_depth)     = 6       (codificado:  0.00)
semilla            = 42
y (R²)             = 0.4821
```

Y queda registrada automáticamente en `resultados.csv`, que acumula todas tus
corridas con las columnas: `corrida, x1_real, x2_real, x1_cod, x2_cod, semilla, y`.

## 3. Factores del experimento

| Factor | Símbolo | Rango natural   | Unidades |
|--------|---------|-----------------|----------|
| Factor 1 | x1    | [0.01, 0.30]    | adimensional |
| Factor 2 | x2    | [2, 10]         | entero (niveles discretos) |

Puedes indicar los factores en **unidades naturales** (por defecto) o en
**escala codificada** [-1, +1] usando el flag `--codificado`. La conversión
entre ambas escalas es lineal, tomando el punto medio del rango natural como
el nivel codificado 0 y los extremos del rango como ±1.

## 4. Respuesta del experimento (y)

`y` representa el rendimiento del proceso medido sobre datos de validación,
en una escala de 0 a 1 donde valores más altos son mejores.

## 5. Parámetro `--semilla`

`--semilla` (por defecto `42`) controla el componente aleatorio interno del
proceso experimental. Puedes cambiarla para explorar la variabilidad natural
del sistema, pero **para un mismo diseño experimental debes usar siempre la
misma semilla en todas tus corridas**, de forma que las diferencias entre
corridas se deban únicamente a los factores x1 y x2 y no a cambios de
semilla.

## 6. Rangos válidos

Los valores de los factores (en unidades naturales) deben estar dentro de:

- x1 ∈ [0.01, 0.30]
- x2 ∈ [2, 10]

**Las corridas fuera de rango son rechazadas** y no se registran en
`resultados.csv`.

## 7. Siguiente paso

Con los datos de `resultados.csv` construirás el análisis RSM.
