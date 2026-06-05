#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repara archivos ERA5-Land descargados como ZIP/GZIP con extensión .nc."""
from pathlib import Path
import zipfile, gzip, shutil
BASE=Path(__file__).resolve().parents[1]
DIR=BASE/'data'/'climate'/'era5land_eber'
def magic(path,n=16):
    with open(path,'rb') as f: return f.read(n)
def is_netcdf(path):
    m=magic(path,8); return m.startswith(b'CDF') or m.startswith(b'\x89HDF\r\n\x1a\n')
def reparar(path):
    m=magic(path,8)
    if is_netcdf(path): print('OK NetCDF:', path.name); return
    if m.startswith(b'PK'):
        print('ZIP detectado:', path.name); tmp=path.with_suffix(''); tmp.mkdir(exist_ok=True)
        with zipfile.ZipFile(path,'r') as z: z.extractall(tmp)
        nc=list(tmp.rglob('*.nc'))
        if not nc: print('  No encontré .nc dentro de', path.name); return
        backup=path.with_suffix('.original_zip'); shutil.move(path, backup); shutil.move(nc[0], path); shutil.rmtree(tmp, ignore_errors=True)
        print('  Reparado:' if is_netcdf(path) else '  Sigue inválido:', path.name); return
    if m.startswith(b'\x1f\x8b'):
        print('GZIP detectado:', path.name); backup=path.with_suffix('.original_gz'); tmp=path.with_suffix('.tmp_nc')
        with gzip.open(path,'rb') as fin, open(tmp,'wb') as fout: shutil.copyfileobj(fin,fout)
        shutil.move(path, backup); shutil.move(tmp, path); print('  Reparado:' if is_netcdf(path) else '  Sigue inválido:', path.name); return
    print('FORMATO DESCONOCIDO:', path.name, 'magic=', m)
def main():
    for path in sorted(DIR.glob('*.nc')): reparar(path)
if __name__=='__main__': main()
