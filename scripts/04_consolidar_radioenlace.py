#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consolida registros FULL_DAY de E0-E5."""
from pathlib import Path
import json, re, pandas as pd, numpy as np
BASE=Path(__file__).resolve().parents[1]
CONFIG=json.loads((BASE/'config.json').read_text(encoding='utf-8'))
RAW=BASE/'data'/'raw'; OUT=BASE/'data'/'processed'; OUT.mkdir(parents=True, exist_ok=True)
SCENARIO_CONFIG={sc:(cfg['frequency_mhz'],cfg['channel_mhz']) for sc,cfg in CONFIG['scenarios'].items()}
def infer_scenario(path:Path):
    s=str(path).upper()
    for sc in ['E0','E1','E2','E3','E4','E5']:
        if re.search(rf'(^|[\\/ _-]){sc}($|[\\/ _-])',s) or sc in s: return sc
    if '5800' in s and '20' in s: return 'E0'
    if '5660' in s and '40' in s: return 'E1'
    if '5660' in s and '80' in s: return 'E2'
    if '5730' in s and '40' in s: return 'E3'
    if '5730' in s and '80' in s: return 'E4'
    if '5805' in s and '40' in s: return 'E5'
    return None
def is_full_day(path:Path):
    n=path.name.upper()
    if 'EPMP_LOCAL' in n: return True
    return 'FULL_DAY' in n and 'RECON' not in n and 'AGG' not in n
def read_csv_flexible(path):
    with open(path,'r',encoding='utf-8',errors='ignore') as f: first=f.readline()
    sep=';' if first.count(';')>first.count(',') else ','
    return pd.read_csv(path,sep=sep,encoding='utf-8',engine='python')
def to_num(x):
    if pd.isna(x): return np.nan
    if isinstance(x,(int,float,np.number)): return float(x)
    s=str(x).strip()
    if s=='' or s.lower() in ['nan','none','null','-']: return np.nan
    mult=1.0
    if s[-1:].upper()=='G': mult=1000.0; s=s[:-1]
    elif s[-1:].upper()=='M': mult=1.0; s=s[:-1]
    elif s[-1:].upper()=='K': mult=0.001; s=s[:-1]
    s=s.replace(',','.'); s=re.sub(r'[^0-9.\-]+','',s)
    try: return float(s)*mult
    except Exception: return np.nan
def clean_metric(series, invalid_zero=True):
    s=pd.to_numeric(series.apply(to_num),errors='coerce')
    return s.mask(s==0,np.nan) if invalid_zero else s
def normalize_e1_e5(df,scenario,source_file):
    cols={c.lower().strip():c for c in df.columns}; tcol=cols.get('timestamp') or cols.get('time') or cols.get('ts')
    out=pd.DataFrame(); out['timestamp']=pd.to_datetime(df[tcol],errors='coerce') if tcol else pd.NaT
    out['escenario']=scenario; out['frecuencia_mhz']=SCENARIO_CONFIG[scenario][0]; out['ancho_canal_mhz']=SCENARIO_CONFIG[scenario][1]; out['source_file']=source_file.name
    mapping={'rssi_dl':['dl_rssi','rssi_dl'],'rssi_ul':['ul_rssi','rssi_ul'],'snr_dl':['dl_snr','snr_dl'],'snr_ul':['ul_snr','snr_ul'],'mcs_dl':['dl_mcs','mcs_dl'],'mcs_ul':['ul_mcs','mcs_ul'],'throughput_dl':['dl_throughput','throughput_dl'],'throughput_ul':['ul_throughput','throughput_ul'],'dl_pkts':['dl_pkts'],'ul_pkts':['ul_pkts'],'dl_kbits':['dl_kbits'],'ul_kbits':['ul_kbits']}
    for outcol,candidates in mapping.items():
        found=next((cols[c] for c in candidates if c in cols),None)
        out[outcol]=clean_metric(df[found], invalid_zero=(outcol not in ['throughput_dl','throughput_ul','dl_pkts','ul_pkts','dl_kbits','ul_kbits'])) if found else np.nan
    return out
def normalize_e0(df,source_file):
    cols={c.lower().strip():c for c in df.columns}; tcol=cols.get('ts') or cols.get('timestamp') or cols.get('time')
    if 'role' in cols:
        role=df[cols['role']].astype(str).str.lower(); mask=role.str.contains('sm|sta|subscriber|suscriptor|station',regex=True,na=False)
        if mask.any(): df=df[mask].copy()
    out=pd.DataFrame(); out['timestamp']=pd.to_datetime(df[tcol],errors='coerce') if tcol else pd.NaT
    out['escenario']='E0'; out['frecuencia_mhz']=SCENARIO_CONFIG['E0'][0]; out['ancho_canal_mhz']=SCENARIO_CONFIG['E0'][1]; out['source_file']=source_file.name
    mapping={'rssi_dl':['sta_dl_rssi','dl_rssi'],'rssi_ul':['sta_ul_rssi','ul_rssi'],'snr_dl':['snr_dl','dl_snr'],'snr_ul':['snr_ul','ul_snr'],'mcs_dl':['mcs_dl','dl_mcs'],'mcs_ul':['mcs_ul','ul_mcs'],'rate_dl':['dl_rate'],'rate_ul':['ul_rate']}
    for outcol,candidates in mapping.items():
        found=next((cols[c] for c in candidates if c in cols),None); out[outcol]=clean_metric(df[found], invalid_zero=(outcol not in ['rate_dl','rate_ul'])) if found else np.nan
    for c in ['throughput_dl','throughput_ul','dl_pkts','ul_pkts','dl_kbits','ul_kbits']: out[c]=np.nan
    return out
def main():
    records=[]; used=[]
    for p in RAW.rglob('*.csv'):
        sc=infer_scenario(p)
        if not sc or not is_full_day(p): continue
        df=read_csv_flexible(p); records.append(normalize_e0(df,p) if sc=='E0' or 'epmp_local' in p.name.lower() else normalize_e1_e5(df,sc,p)); used.append(str(p.relative_to(BASE)))
    if not records: raise RuntimeError('No se encontraron CSV FULL_DAY en data/raw/E0...E5')
    dataset=pd.concat(records,ignore_index=True).dropna(subset=['timestamp']).copy()
    dataset['fecha']=dataset['timestamp'].dt.date.astype(str); dataset['hora']=dataset['timestamp'].dt.strftime('%H:%M:%S')
    order=['timestamp','fecha','hora','escenario','frecuencia_mhz','ancho_canal_mhz','rssi_dl','rssi_ul','snr_dl','snr_ul','mcs_dl','mcs_ul','throughput_dl','throughput_ul','rate_dl','rate_ul','dl_pkts','ul_pkts','dl_kbits','ul_kbits','source_file']
    for c in order:
        if c not in dataset.columns: dataset[c]=np.nan
    dataset=dataset[order].sort_values(['escenario','timestamp']); dataset.to_csv(OUT/'dataset_escenarios_full_day.csv',index=False,encoding='utf-8-sig')
    metrics=['rssi_dl','rssi_ul','snr_dl','snr_ul','mcs_dl','mcs_ul','throughput_dl','throughput_ul','rate_dl','rate_ul']; rows=[]
    for sc,g in dataset.groupby('escenario'):
        row={'escenario':sc,'frecuencia_mhz':SCENARIO_CONFIG[sc][0],'ancho_canal_mhz':SCENARIO_CONFIG[sc][1],'n_registros':len(g),'fecha_inicio':g['fecha'].min(),'fecha_fin':g['fecha'].max(),'dias_unicos':g['fecha'].nunique()}
        for m in metrics:
            s=pd.to_numeric(g[m],errors='coerce').dropna(); row[f'{m}_media']=s.mean() if len(s) else np.nan; row[f'{m}_de']=s.std(ddof=1) if len(s)>1 else np.nan; row[f'{m}_min']=s.min() if len(s) else np.nan; row[f'{m}_p5']=s.quantile(.05) if len(s) else np.nan; row[f'{m}_p50']=s.quantile(.50) if len(s) else np.nan; row[f'{m}_p95']=s.quantile(.95) if len(s) else np.nan; row[f'{m}_max']=s.max() if len(s) else np.nan
        rows.append(row)
    summary=pd.DataFrame(rows).sort_values('escenario'); summary.to_csv(OUT/'resumen_escenarios.csv',index=False,encoding='utf-8-sig')
    summary[['escenario','frecuencia_mhz','ancho_canal_mhz','n_registros','dias_unicos','rssi_dl_media','rssi_dl_de','snr_dl_media','snr_dl_de','mcs_dl_media','mcs_dl_de']].to_csv(OUT/'tabla_4_1_descriptivos_principales.csv',index=False,encoding='utf-8-sig')
    (OUT/'used_files.txt').write_text('\n'.join(used),encoding='utf-8')
    print('Dataset generado:',OUT/'dataset_escenarios_full_day.csv'); print('Filas:',len(dataset)); print('Archivos usados:',len(used))
if __name__=='__main__': main()
