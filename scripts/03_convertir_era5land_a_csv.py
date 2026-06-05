#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte NetCDF ERA5-Land a CSV horario consolidado."""
from pathlib import Path
import json, numpy as np, pandas as pd, xarray as xr
BASE=Path(__file__).resolve().parents[1]
CONFIG=json.loads((BASE/'config.json').read_text(encoding='utf-8'))
INPUT_DIR=BASE/'data'/'climate'/'era5land_eber'
OUTPUT_FILE=INPUT_DIR/'era5land_2026-02-19_a_2026-06-01.csv'
START_LIMA=CONFIG['study_period']['start_lima']; END_LIMA=CONFIG['study_period']['end_lima_current']; LIMA_TZ=CONFIG['timezone']
def open_dataset(nc_files): return xr.open_mfdataset(nc_files, combine='by_coords', engine='netcdf4')
def convert_site(site_name):
    files=sorted(INPUT_DIR.glob(f'era5land_{site_name}_2026-*.nc'))
    if not files: raise FileNotFoundError(f'No se encontraron NetCDF para {site_name}')
    print(f'Procesando {site_name}: {len(files)} archivos')
    ds=open_dataset(files)
    if 'latitude' in ds.dims and 'longitude' in ds.dims: ds=ds.mean(dim=['latitude','longitude'], skipna=True)
    time_name='valid_time' if 'valid_time' in ds.coords else 'time'
    data={'time_utc':pd.to_datetime(ds[time_name].values, utc=True)}; prefix=site_name.lower()
    if 't2m' in ds: data[f'{prefix}_temp_c']=ds['t2m'].values-273.15
    if 'd2m' in ds: data[f'{prefix}_dewpoint_c']=ds['d2m'].values-273.15
    if 'tp' in ds: data[f'{prefix}_precip_mm']=ds['tp'].values*1000.0
    if 'sp' in ds: data[f'{prefix}_press_hpa']=ds['sp'].values/100.0
    if 'u10' in ds and 'v10' in ds: data[f'{prefix}_wind_ms']=np.sqrt(ds['u10'].values**2+ds['v10'].values**2)
    df=pd.DataFrame(data); df['time_lima']=df['time_utc'].dt.tz_convert(LIMA_TZ); return df
def main():
    df_mid=convert_site('MID'); df_sm=convert_site('SM')
    df=pd.merge(df_mid, df_sm, on=['time_utc','time_lima'], how='outer').sort_values('time_utc')
    start=pd.Timestamp(START_LIMA,tz=LIMA_TZ); end=pd.Timestamp(END_LIMA,tz=LIMA_TZ)
    df=df[(df['time_lima']>=start)&(df['time_lima']<=end)].copy()
    df['precip_mm']=df['mid_precip_mm']; df['condicion_lluvia']=np.where(df['precip_mm']>0,'Con lluvia','Sin lluvia')
    df.to_csv(OUTPUT_FILE,index=False,encoding='utf-8-sig')
    print('Archivo generado:', OUTPUT_FILE); print('Filas:', len(df)); print('Columnas:', df.columns.tolist())
if __name__=='__main__': main()
