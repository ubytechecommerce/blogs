@echo off
cd /d "%~dp0"
git add .
git commit -m "Atualização automática"
git push
pause