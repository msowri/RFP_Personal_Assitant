@echo off
REM Run database migrations using Alembic in the backend virtual environment.
cd /d "%~dp0"
call venv\Scripts\activate
python -m alembic upgrade head
