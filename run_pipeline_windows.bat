@echo off
echo Instalando dependencias...
python -m pip install -r requirements.txt

echo.
echo Ejecutando flujo reproducible...
python scripts\run_all.py

echo.
echo Proceso finalizado.
pause
