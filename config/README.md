# Configuración de la unidad U4

Este archivo explica `config.yaml`.

## Qué contiene

| Bloque | Uso |
|---|---|
| `unidad` | Identificación y lista de temas del programa |
| `evaluacion` | Tolerancia de las celdas de autoevaluación; sin backend |
| `datos` | Datasets de los ejemplos del libro usados en los cuadernos |
| `aplicaciones` | Datos de las fichas de robot y sensor |

## Cómo se usa

Los cuadernos leen los datos directamente de sus celdas para que sean
autosuficientes; `config.yaml` es la **fuente de verdad** para el profesor y
para los scripts de verificación. Si cambias un dataset aquí, actualízalo
también en el cuaderno y en `tests/test_ajuste_curvas.py`.

## Backend

Esta unidad no tiene Apps Script. Si se conecta uno, copia el patrón de
`U3_Repo/config/config.yaml`:

```yaml
evaluacion:
  webhook_token: "..."
  apps_script_url: "..."
  max_intentos: 5
```

El motor acepta además variables de entorno para no escribir secretos en el
repo: `MN_APPS_URL`, `MN_TOKEN` y `MN_REPO` (ruta del repositorio).
