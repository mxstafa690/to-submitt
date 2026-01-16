@echo off
cls
echo ====================================
echo FitTrack - MySQL Version
echo ====================================
echo.
echo IMPORTANT: Make sure MySQL is running and fittrack database exists!
echo.

cd /d "c:\Users\Win10 Pro\Downloads\FitTrack-5\FitTrack\server"

echo [1/3] Installing dependencies...
python -m pip install -q Flask==3.0.0 Flask-CORS==4.0.0 SQLAlchemy==2.0.23 pymysql==1.1.0 "pydantic>=2.10.0" cryptography==41.0.7 Werkzeug==3.0.1
if errorlevel 1 goto error
echo OK - Dependencies installed
echo.

echo [2/3] Seeding MySQL database...
python seed.py
if errorlevel 1 goto error
echo.

echo [3/3] Starting Flask server...
echo Server starting at http://127.0.0.1:5000
echo Press Ctrl+C to stop
echo.
python app.py
goto end

:error
echo.
echo ERROR: Something went wrong!
pause
exit /b 1

:end
