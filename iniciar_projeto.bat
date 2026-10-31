@echo off
cd /d "%~dp0"
echo Inicie primeiro Backend\iniciar_backend.bat para usar a API da aula.
python main.py
if errorlevel 1 pause
