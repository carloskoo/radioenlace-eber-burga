#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Une dataset_escenarios_full_day.csv con ERA5-Land por hora Lima."""
from pathlib import Path
import pandas as pd, numpy as np
BASE=Path(__file__).resolve().parents[1]
PROCESSED=BASE/'data'/'processed'; CLIMATE=BASE/'data'/'climate'/'era5land_eber'
radio=pd.read_csv(PROCESSED/'dataset_escenarios_full_day.csv')
era5=pd.read_csv(CLIMATE/'era5land_2026-02-19_a_2026-06-01.csv')
radio['timestamp']=pd.to_datetime(radio['timestamp'],errors='coerce',utc=True)
radio['time_lima_radio']=radio['timestamp'].dt.tz_convert('America/Lima')
radio['hora_merge']=radio['time_lima_radio'].dt.strftime('%Y-%m-%d %H')
era5['time_lima']=pd.to_datetime(era5['time_lima'],errors='coerce',utc=True)
era5['time_lima_era5']=era5['time_lima'].dt.tz_convert('America/Lima')
era5['hora_merge']=era5['time_lima_era5'].dt.strftime('%Y-%m-%d %H')
precip_col=next((c for c in ['precip_mm','mid_precip_mm','sm_precip_mm'] if c in era5.columns),None)
if precip_col is None: raise ValueError('No se encontró columna de precipitación en ERA5.')
era_cols=['hora_merge',precip_col]+[c for c in ['mid_temp_c','mid_dewpoint_c','mid_press_hpa','mid_wind_ms','sm_temp_c','sm_dewpoint_c','sm_press_hpa','sm_wind_ms'] if c in era5.columns]
era5_merge=era5[era_cols].copy().rename(columns={precip_col:'precip_mm'})
df=pd.merge(radio,era5_merge,on='hora_merge',how='left')
df['condicion_lluvia']=np.where(df['precip_mm'].isna(),'Sin dato climático',np.where(df['precip_mm']>0,'Con lluvia','Sin lluvia'))
out=PROCESSED/'dataset_radio_clima.csv'; df.to_csv(out,index=False,encoding='utf-8-sig')
print('Archivo generado:',out); print('Filas:',len(df)); print('Registros con clima:',df['precip_mm'].notna().sum()); print('Registros sin clima:',df['precip_mm'].isna().sum())
