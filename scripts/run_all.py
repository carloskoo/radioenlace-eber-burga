#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
steps=['02_reparar_nc.py','03_convertir_era5land_a_csv.py','04_consolidar_radioenlace.py','05_merge_radio_era5.py','06_analisis_precipitacion.py','07_figuras_estabilidad.py']
for script in steps:
    path=BASE/'scripts'/script
    print('\n'+'='*70); print('Ejecutando:',script); print('='*70)
    subprocess.run([sys.executable,str(path)],check=True)
print('\nFlujo completo finalizado.')
