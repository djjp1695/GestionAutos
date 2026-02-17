@echo off

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Your commands after activation
fastapi run
