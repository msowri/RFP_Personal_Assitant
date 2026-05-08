@echo off
REM Create a new Alembic migration revision with autogenerate.
cd /d "%~dp0"
if "%~1"=="" (
  echo Usage: makemigration.bat "Migration message"
  exit /b 1
)
call venv\Scripts\activate
python -m alembic revision --autogenerate -m "%~1"
