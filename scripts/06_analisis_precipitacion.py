#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera tablas para la sección 4.3."""
from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
PROCESSED=BASE/'data'/'processed'; TABLES=BASE/'outputs'/'tables'; TABLES.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(PROCESSED/'dataset_radio_clima.csv'); df=df[df['precip_mm'].notna()].copy()
metricas=['rssi_dl','snr_dl','mcs_dl','throughput_dl']
tabla_conteo=df.groupby('condicion_lluvia').size().reset_index(name='n_registros'); tabla_conteo['porcentaje']=(tabla_conteo['n_registros']/tabla_conteo['n_registros'].sum()*100).round(2); tabla_conteo.to_csv(TABLES/'tabla_4_3_conteo_lluvia.csv',index=False,encoding='utf-8-sig')
tabla_desempeno=df.groupby('condicion_lluvia')[metricas].agg(['mean','std','median']); tabla_desempeno.to_csv(TABLES/'tabla_4_4_desempeno_lluvia.csv',encoding='utf-8-sig')
correlaciones=[]
for m in metricas:
    tmp=df[['precip_mm',m]].dropna()
    if len(tmp)>0: correlaciones.append({'variable':m,'rho_spearman':tmp['precip_mm'].corr(tmp[m],method='spearman'),'n':len(tmp)})
tabla_corr=pd.DataFrame(correlaciones); tabla_corr.to_csv(TABLES/'tabla_4_5_correlacion_precipitacion.csv',index=False,encoding='utf-8-sig')
print('Tablas generadas en:',TABLES); print(tabla_conteo); print(tabla_corr)
