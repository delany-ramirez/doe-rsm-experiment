# Instrucciones del proyecto — Búsqueda de la superficie de respuesta

Este documento describe, a grandes rasgos, la ruta que debes seguir para
explorar el proceso experimental y llegar a su punto óptimo mediante
Metodología de Superficie de Respuesta (RSM). No sigas los pasos de forma
mecánica: en cada fase debes analizar tus datos antes de decidir el
siguiente movimiento, igual que en un experimento real.

Recuerda: toda tu campaña experimental (todas las fases) debe usar **la
misma semilla** (`--semilla`) para que las diferencias entre corridas se
deban solo a x1 y x2.

---

## Fase 1 — Diseño inicial de primer orden (4 puntos)

Comienza con un diseño factorial 2² completo, es decir, las cuatro
combinaciones extremas de los factores en escala codificada:

| Corrida | x1 (cod) | x2 (cod) | x1 natural (learning_rate) | x2 natural (max_depth) |
|---------|----------|----------|------------------------------|--------------------------|
| 1       | -1       | -1       | 0.01                         | 2                        |
| 2       | +1       | -1       | 0.30                         | 2                        |
| 3       | -1       | +1       | 0.01                         | 10                       |
| 4       | +1       | +1       | 0.30                         | 10                       |

Estos cuatro puntos son las esquinas del espacio experimental completo
(los extremos de los rangos válidos de x1 y x2). Puedes ejecutarlos usando
directamente los valores naturales, o con el flag `--codificado`, por
ejemplo:

```bash
uv run corrida --x1 -1 --x2 -1 --codificado
uv run corrida --x1  1 --x2 -1 --codificado
uv run corrida --x1 -1 --x2  1 --codificado
uv run corrida --x1  1 --x2  1 --codificado
```

Con estos cuatro resultados, ajusta un **modelo lineal (de primer orden)**:

```
y = b0 + b1·x1 + b2·x2
```

**Recomendación:** agrega 2 o 3 réplicas en el punto central (x1=0, x2=0
codificado) antes de continuar. Te sirven para estimar el error puro y
detectar si hay curvatura importante — si la hay, es una señal de que ya
estás cerca de la región óptima y el modelo lineal no será suficiente.

---

## Fase 2 — Camino de máximo ascenso (steepest ascent)

Si el modelo de primer orden es adecuado (no hay curvatura fuerte) y los
coeficientes b1, b2 indican una dirección clara de mejora:

1. Calcula la dirección de ascenso a partir de los coeficientes del modelo.
2. Diseña una serie de corridas siguiendo esa dirección, alejándote paso a
   paso del punto central inicial (en unidades naturales, respetando
   siempre los rangos válidos de x1 y x2).
3. Ejecuta cada punto del camino y registra cómo cambia y.
4. Detente cuando la respuesta deje de mejorar (o quede claro que llegaste
   a una región de curvatura, o que tocaste el borde del rango permitido).

El mejor punto que encuentres en este camino será el nuevo centro para la
siguiente fase.

---

## Fase 3 — Diseño de segundo orden alrededor del óptimo

Alrededor del mejor punto encontrado en la Fase 2, construye un diseño que
permita ajustar un **modelo de segundo orden** (por ejemplo, un diseño
central compuesto: los puntos factoriales, puntos axiales y varias
réplicas del punto central), siempre dentro de los rangos válidos:

- x1 ∈ [0.01, 0.30]
- x2 ∈ [2, 10]

Ejecuta todas las corridas de este diseño con la misma semilla que has
usado en todo el proyecto.

---

## Fase 4 — Ajuste del modelo de segundo orden y análisis canónico

Con los datos del diseño de la Fase 3, ajusta el modelo completo:

```
y = b0 + b1·x1 + b2·x2 + b11·x1² + b22·x2² + b12·x1·x2
```

Luego:

1. Encuentra el punto estacionario del modelo.
2. Realiza el análisis canónico (signos y magnitud de los valores propios)
   para determinar si el punto estacionario es un máximo, un mínimo o un
   punto de silla.
3. Verifica que el punto óptimo esté dentro de los rangos válidos de x1 y
   x2; si no lo está, deberás decidir cómo acotar tu búsqueda dentro de la
   región experimental.

---

## Fase 5 — Confirmación del óptimo

Ejecuta corridas adicionales en el punto óptimo estimado (y, si quieres
evaluar su robustez, en puntos cercanos) y compara la respuesta observada
contra la predicha por tu modelo de segundo orden.

---

## Entregable

Tu análisis debe basarse en el archivo `resultados.csv` acumulado durante
todas las fases, y debe incluir como mínimo:

- El modelo de primer orden y la decisión tomada a partir de él.
- Las corridas del camino de máximo ascenso y su justificación.
- El diseño y modelo de segundo orden.
- El análisis canónico y el punto óptimo identificado.
- La corrida (o corridas) de confirmación del óptimo.
