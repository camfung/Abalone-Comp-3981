@echo off
setlocal

cd /d "%~dp0\.."

echo === Abalone Game Build Script ===
echo.

:: Check for PyInstaller (prefer py -3.11 where it is installed)
set PYTHON=py -3.11
%PYTHON% -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    set PYTHON=python
    %PYTHON% -m PyInstaller --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: PyInstaller not found. Install it with:
        echo   pip install pyinstaller
        exit /b 1
    )
)

:: Build executable
echo [1/2] Building executable with PyInstaller...
%PYTHON% -m PyInstaller installer\Abalone_Game.spec ^
    --distpath dist ^
    --workpath build\pyinstaller ^
    --clean
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller build failed.
    exit /b 1
)
echo Done. Executable folder: dist\Abalone_Game\
echo.

:: Build installer (optional - requires Inno Setup 6)
echo [2/2] Building installer with Inno Setup...
set ISCC=
if exist "%PROGRAMFILES(X86)%\Inno Setup 6\ISCC.exe" set ISCC=%PROGRAMFILES(X86)%\Inno Setup 6\ISCC.exe
if exist "%PROGRAMFILES%\Inno Setup 6\ISCC.exe"      set ISCC=%PROGRAMFILES%\Inno Setup 6\ISCC.exe

if "%ISCC%"=="" (
    echo SKIP: Inno Setup 6 not found. Download from https://jrsoftware.org/isinfo.php
    echo       The executable folder at dist\Abalone_Game\ is still usable without an installer.
) else (
    "%ISCC%" installer\installer.iss
    if %errorlevel% neq 0 (
        echo ERROR: Inno Setup build failed.
        exit /b 1
    )
    echo Done. Installer: dist\installer\Abalone_Game_Setup.exe
)

echo.
echo === Build complete ===
endlocal
