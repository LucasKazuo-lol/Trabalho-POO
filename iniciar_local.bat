@echo off
cd /d "%~dp0"
python main.py --local
if errorlevel 1 pause
