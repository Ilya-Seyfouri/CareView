@echo off
REM CareView Database Backup Script for Windows

echo.
echo ========================================
echo    CareView Database Backup System
echo ========================================
echo.

REM Load environment variables from .env if it exists
if exist .env (
    echo Loading database settings from .env file...
    for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
        if not "%%a"=="" if not "%%b"=="" set %%a=%%b
    )
) else (
    echo Warning: .env file not found, using default values
)

REM Database configuration with defaults
if not defined DB_HOST set DB_HOST=localhost
if not defined DB_PORT set DB_PORT=5432

if not defined DB_NAME set DB_NAME=careview
if not defined DB_USER set DB_USER=admin
if not defined DB_PASSWORD set DB_PASSWORD=MySecurePass123

REM Create backup directory
if not exist "backups" (
    echo Creating backup directory...
    mkdir backups
)

REM Get current date/time for filename
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%"
set "Min=%dt:~10,2%"
set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%%MM%%DD%_%HH%%Min%%Sec%"

set BACKUP_FILE=backups\careview_backup_%timestamp%.sql

echo.
echo Starting backup...
echo   Database: %DB_NAME%
echo   Host: %DB_HOST%:%DB_PORT%
echo   User: %DB_USER%
echo   File: %BACKUP_FILE%
echo.

REM Check if pg_dump is available
pg_dump --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pg_dump not found!
    echo Please install PostgreSQL client tools:
    echo https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)

REM Set password for pg_dump (avoids password prompt)
set PGPASSWORD=%DB_PASSWORD%

REM Create the backup
echo Creating backup file...
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% --verbose --clean --create --if-exists > "%BACKUP_FILE%" 2>backup_error.log

REM Check if backup was successful
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Backup completed successfully!
    echo ========================================
    echo   File: %BACKUP_FILE%

    REM Show file size
    for %%F in ("%BACKUP_FILE%") do (
        echo   Size: %%~zF bytes
        if %%~zF gtr 1000 (
            echo   Status: Good - file contains data
        ) else (
            echo   Status: Warning - file seems small
        )
    )

    echo.
    echo Backup Information:
    echo   Created: %date% %time%
    echo   Tables: users, clients, schedules, visit_logs, audit_logs
    echo.
    echo To restore this backup:
    echo   psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d postgres -f "%BACKUP_FILE%"

) else (
    echo.
    echo ========================================
    echo   Backup FAILED!
    echo ========================================
    echo Check backup_error.log for details:
    type backup_error.log
)

REM Clear password from environment
set PGPASSWORD=

echo.
echo Press any key to exit...
pause >nul