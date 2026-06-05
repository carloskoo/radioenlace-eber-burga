# Guía rápida para subir a GitHub

```bash
cd radioenlace-eber-burga-github
git init
git add .
git commit -m "Initial reproducible radio link dataset pipeline"
git branch -M main
git remote add origin https://github.com/TU\_USUARIO/radioenlace-eber-burga.git
git push -u origin main
```

Si los archivos crudos o NetCDF son muy pesados, subir solo scripts, README, requirements, config, data/processed y outputs.



\# Guía de Uso y Reproducción del Proyecto



\## Descripción



Este repositorio contiene los datos, scripts y resultados utilizados para la investigación:



\*\*“Evaluación de la influencia de la configuración técnica sobre el desempeño operativo de un radioenlace punto a punto bajo condiciones reales de operación”\*\*



El objetivo del repositorio es garantizar la reproducibilidad del procesamiento de datos, desde la consolidación de la telemetría del radioenlace hasta la generación de tablas y figuras utilizadas en la tesis.



\---



\# Estructura del proyecto



```text

radioenlace-eber-burga-github

│

├── data

│   ├── raw

│   │   ├── E0

│   │   ├── E1

│   │   ├── E2

│   │   ├── E3

│   │   ├── E4

│   │   └── E5

│   │

│   ├── climate

│   │   └── era5land\_eber

│   │

│   └── processed

│

├── outputs

│   ├── figures

│   └── tables

│

├── scripts

│

├── docs

│

├── README.md

├── requirements.txt

├── config.json

└── run\_pipeline\_windows.bat

```



\---



\# Escenarios experimentales



Durante la investigación se evaluaron seis configuraciones espectrales del radioenlace.



| Escenario | Frecuencia (MHz) | Canal (MHz) |

| --------- | ---------------- | ----------- |

| E0        | 5800             | 20          |

| E1        | 5660             | 40          |

| E2        | 5660             | 80          |

| E3        | 5730             | 40          |

| E4        | 5730             | 80          |

| E5        | 5805             | 40          |



\---



\# Periodo de estudio



Fecha de inicio:



```text

19/02/2026

```



Fecha de finalización:



```text

01/06/2026

```



\---



\# Variables analizadas



\## Variables técnicas



\* RSSI Downlink (dBm)

\* RSSI Uplink (dBm)

\* SNR Downlink (dB)

\* SNR Uplink (dB)

\* MCS Downlink

\* MCS Uplink

\* Throughput Downlink (Mbps)

\* Throughput Uplink (Mbps)



\## Variables climatológicas



Obtenidas desde ERA5-Land:



\* Precipitación (mm/h)

\* Temperatura (°C)

\* Punto de rocío (°C)

\* Presión superficial (hPa)

\* Velocidad del viento (m/s)



\---



\# Flujo de procesamiento



\## Paso 1. Descarga de datos climatológicos



Ejecutar:



```bash

python scripts/01\_descargar\_era5land.py

```



Este script descarga los datos horarios ERA5-Land para los puntos geográficos definidos en el archivo `config.json`.



\---



\## Paso 2. Reparación de archivos descargados



Algunas descargas de Copernicus pueden llegar comprimidas con extensión `.nc`.



Ejecutar:



```bash

python scripts/02\_reparar\_nc.py

```



\---



\## Paso 3. Conversión de ERA5-Land a CSV



Ejecutar:



```bash

python scripts/03\_convertir\_era5land\_a\_csv.py

```



Resultado:



```text

data/climate/era5land\_eber/

era5land\_2026-02-19\_a\_2026-06-01.csv

```



\---



\## Paso 4. Consolidación de telemetría del radioenlace



Ejecutar:



```bash

python scripts/04\_consolidar\_radioenlace.py

```



Resultado:



```text

data/processed/

dataset\_escenarios\_full\_day.csv

```



\---



\## Paso 5. Integración radioenlace + clima



Ejecutar:



```bash

python scripts/05\_merge\_radio\_era5.py

```



Resultado:



```text

data/processed/

dataset\_radio\_clima.csv

```



\---



\## Paso 6. Análisis de precipitación



Ejecutar:



```bash

python scripts/06\_analisis\_precipitacion.py

```



Resultados:



```text

outputs/tables/

tabla\_4\_3\_conteo\_lluvia.csv

tabla\_4\_4\_desempeno\_lluvia.csv

tabla\_4\_5\_correlacion\_precipitacion.csv

```



\---



\## Paso 7. Análisis de estabilidad operativa



Ejecutar:



```bash

python scripts/07\_figuras\_estabilidad.py

```



Resultados:



```text

outputs/tables/

tabla\_4\_6\_estabilidad\_por\_escenario.csv

```



y las figuras:



```text

outputs/figures/

fig\_5\_cv\_rssi.png

fig\_6\_boxplot\_rssi.png

fig\_7\_cv\_mcs.png

fig\_8\_cv\_throughput.png

```



\---



\# Ejecución completa



Para reproducir todo el flujo automáticamente:



```bash

python scripts/run\_all.py

```



o en Windows:



```bash

run\_pipeline\_windows.bat

```



\---



\# Resultados principales obtenidos



El estudio permitió:



\* Comparar seis configuraciones espectrales diferentes.

\* Evaluar métricas RSSI, SNR, MCS y throughput en condiciones reales.

\* Analizar la estabilidad temporal del radioenlace.

\* Integrar datos climatológicos horarios provenientes de ERA5-Land.

\* Determinar la relación entre precipitación y desempeño técnico.

\* Identificar configuraciones con mejor estabilidad operativa.



\---



\# Reproducibilidad



Todos los resultados presentados en la tesis pueden regenerarse utilizando exclusivamente:



1\. Los archivos originales de telemetría.

2\. Los archivos climatológicos ERA5-Land.

3\. Los scripts incluidos en este repositorio.



Esto garantiza la trazabilidad y reproducibilidad completa del análisis realizado.



