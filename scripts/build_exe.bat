@echo off
setlocal
cd /d %~dp0\..
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --noconfirm --windowed --name "Convairo Pro" --add-data "app\translations;app\translations" --add-data "assets;assets" main.py
echo.
echo EXE created in dist\Convairo Pro\
pause
