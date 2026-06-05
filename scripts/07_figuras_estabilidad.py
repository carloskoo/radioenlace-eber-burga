#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera tablas y figuras de estabilidad operativa."""
from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt, numpy as np
BASE=Path(__file__).resolve().parents[1]
PROCESSED=BASE/'data'/'processed'; FIGURES=BASE/'outputs'/'figures'; TABLES=BASE/'outputs'/'tables'
FIGURES.mkdir(parents=True,exist_ok=True); TABLES.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(PROCESSED/'dataset_radio_clima.csv')
metricas=['rssi_dl','mcs_dl','throughput_dl']; resumen=[]
for esc,g in df.groupby('escenario'):
    fila={'escenario':esc}
    for m in metricas:
        x=g[m].dropna()
        if len(x)==0: fila[f'{m}_mean']=np.nan; fila[f'{m}_std']=np.nan; fila[f'{m}_cv']=np.nan
        else:
            media=x.mean(); de=x.std(); cv=abs(de/media)*100 if media!=0 else np.nan
            fila[f'{m}_mean']=media; fila[f'{m}_std']=de; fila[f'{m}_cv']=cv
    resumen.append(fila)
res=pd.DataFrame(resumen).sort_values('escenario'); res.to_csv(TABLES/'tabla_4_6_estabilidad_por_escenario.csv',index=False,encoding='utf-8-sig')
plt.rcParams['figure.dpi']=150; plt.rcParams['savefig.dpi']=300; plt.rcParams['font.family']='Arial'; plt.rcParams['axes.edgecolor']='#333333'; plt.rcParams['axes.linewidth']=0.8; plt.rcParams['grid.color']='#D0D0D0'; plt.rcParams['grid.linewidth']=0.6; plt.rcParams['grid.alpha']=0.7
def savefig(name):
    plt.tight_layout(); plt.savefig(FIGURES/f'{name}.png',bbox_inches='tight'); plt.savefig(FIGURES/f'{name}.pdf',bbox_inches='tight'); plt.close()
def bar_cv(col,title,ylabel,name,offset,fmt):
    fig,ax=plt.subplots(figsize=(8,4.6)); plot=res.dropna(subset=[col])
    ax.bar(plot['escenario'],plot[col],edgecolor='black',linewidth=0.8)
    ax.set_title(title,fontsize=13,weight='bold'); ax.set_xlabel('Escenario experimental'); ax.set_ylabel(ylabel); ax.grid(axis='y')
    for i,v in enumerate(plot[col]): ax.text(i,v+offset,fmt.format(v),ha='center',va='bottom',fontsize=9)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); savefig(name)
bar_cv('rssi_dl_cv','Coeficiente de variación del RSSI descendente','CV RSSI DL (%)','fig_5_cv_rssi',0.03,'{:.2f}%')
fig,ax=plt.subplots(figsize=(8,4.8)); orden=sorted(df['escenario'].dropna().unique()); data=[df.loc[df['escenario']==esc,'rssi_dl'].dropna() for esc in orden]
bp=ax.boxplot(data,tick_labels=orden,patch_artist=True,showmeans=True,meanline=True,widths=0.55,flierprops=dict(marker='o',markersize=3,alpha=0.45),medianprops=dict(color='black',linewidth=1.3),meanprops=dict(color='black',linewidth=1.1,linestyle='--'),boxprops=dict(linewidth=0.9),whiskerprops=dict(linewidth=0.9),capprops=dict(linewidth=0.9))
for box in bp['boxes']: box.set_facecolor('#E8EEF7'); box.set_edgecolor('black')
ax.set_title('Distribución del RSSI descendente por escenario',fontsize=13,weight='bold'); ax.set_xlabel('Escenario experimental'); ax.set_ylabel('RSSI DL (dBm)'); ax.grid(axis='y'); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); savefig('fig_6_boxplot_rssi')
bar_cv('mcs_dl_cv','Coeficiente de variación del MCS descendente','CV MCS DL (%)','fig_7_cv_mcs',0.04,'{:.2f}%')
bar_cv('throughput_dl_cv','Coeficiente de variación del throughput descendente observado','CV Throughput DL (%)','fig_8_cv_throughput',1.0,'{:.1f}%')
print('Tabla y figuras generadas.'); print('Tabla:',TABLES/'tabla_4_6_estabilidad_por_escenario.csv'); print('Figuras:',FIGURES)
