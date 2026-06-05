#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Descarga ERA5-Land desde Copernicus CDS para MID y SM."""
import json
from pathlib import Path
import cdsapi
BASE = Path(__file__).resolve().parents[1]
CONFIG = json.loads((BASE/'config.json').read_text(encoding='utf-8'))
OUT_DIR = BASE/'data'/'climate'/'era5land_eber'
OUT_DIR.mkdir(parents=True, exist_ok=True)
POINTS={'MID':CONFIG['coordinates']['mid'], 'SM':CONFIG['coordinates']['sm']}
MONTHS=[('2026','02'),('2026','03'),('2026','04'),('2026','05')]  # agregar ('2026','06') cuando esté disponible
VARIABLES=['2m_temperature','2m_dewpoint_temperature','total_precipitation','surface_pressure','10m_u_component_of_wind','10m_v_component_of_wind']
HOURS=[f'{h:02d}:00' for h in range(24)]
def days_for_month(year, month):
    if month=='02': return [f'{d:02d}' for d in range(1,29)]
    if month in ['04','06']: return [f'{d:02d}' for d in range(1,31)]
    return [f'{d:02d}' for d in range(1,32)]
def build_area(lat, lon, box_deg=0.20):
    return [lat+box_deg/2, lon-box_deg/2, lat-box_deg/2, lon+box_deg/2]
def download_month(point_name, lat, lon, year, month):
    output_file=OUT_DIR/f'era5land_{point_name}_{year}-{month}_lat{lat:.4f}_lon{lon:.4f}.nc'
    if output_file.exists() and output_file.stat().st_size>0:
        print('Ya existe:', output_file); return
    print(f'Descargando {point_name} {year}-{month}...')
    request={'variable':VARIABLES,'year':year,'month':month,'day':days_for_month(year,month),'time':HOURS,'area':build_area(lat,lon),'data_format':'netcdf','download_format':'unarchived'}
    cdsapi.Client().retrieve('reanalysis-era5-land', request, str(output_file))
    print('Guardado:', output_file)
def main():
    for point_name, point in POINTS.items():
        for year, month in MONTHS:
            download_month(point_name, point['lat'], point['lon'], year, month)
    print('Descarga ERA5-Land finalizada.')
if __name__=='__main__': main()
