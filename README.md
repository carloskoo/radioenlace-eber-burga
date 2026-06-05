# Radioenlace Eber Burga — Dataset y análisis reproducible

Repositorio para consolidar, procesar y analizar registros de telemetría de un radioenlace punto a punto evaluado bajo seis escenarios experimentales.

## Escenarios evaluados

| Escenario | Frecuencia | Ancho de canal | Fuente |
|---|---:|---:|---|
| E0 | 5800 MHz | 20 MHz | Registro local ePMP |
| E1 | 5660 MHz | 40 MHz | cnMaestro |
| E2 | 5660 MHz | 80 MHz | cnMaestro |
| E3 | 5730 MHz | 40 MHz | cnMaestro |
| E4 | 5730 MHz | 80 MHz | cnMaestro |
| E5 | 5805 MHz | 40 MHz | cnMaestro |

## Estructura

```text
radioenlace-eber-burga-github/
├── config.json
├── requirements.txt
├── README.md
├── data/
│   ├── raw/E0 ... raw/E5
│   ├── climate/era5land_eber/
│   └── processed/
├── outputs/figures/
├── outputs/tables/
└── scripts/
```

## Instalación

```bash
pip install -r requirements.txt
```

## Flujo recomendado

1. Colocar los CSV crudos de E0–E5 dentro de `data/raw/E0` ... `data/raw/E5`.
2. Colocar o descargar los NetCDF ERA5-Land en `data/climate/era5land_eber`.
3. Ejecutar:

```bash
python scripts/run_all.py
```

## Productos generados

```text
data/processed/dataset_escenarios_full_day.csv
data/processed/resumen_escenarios.csv
data/processed/dataset_radio_clima.csv
outputs/tables/*.csv
outputs/figures/*.png
outputs/figures/*.pdf
```

## Nota metodológica

El throughput registrado representa tráfico efectivamente observado durante el monitoreo y no la capacidad máxima teórica del enlace. Para E0, el formato local no contiene throughput comparable con cnMaestro.
