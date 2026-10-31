@echo off
cd /d "%~dp0"
if not exist "%~dp0BackendEstudoAPI.exe" (
    echo Copie para esta pasta os arquivos do backend fornecidos na aula.
    echo Consulte o arquivo README.md desta pasta para ver a lista.
    pause
    exit /b 1
)
"%~dp0BackendEstudoAPI.exe" %*
if errorlevel 1 pause
