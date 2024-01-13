@echo off

set "INSTALL_DIR=C:\Users\%USERNAME%\Documents\spyke"

python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installez Python3.
    exit /b
)

echo Installation des modules necessaires...
pip3 install -r requirements.txt
if %errorlevel% neq 0 (
    echo Erreur inattendue lors de la copie des fichiers!
    exit /b
)
echo Fait.

echo Copie des fichiers...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo @echo off > ".\spyke\launching.bat"
echo python3 %INSTALL_DIR%\main.py >> ".\spyke\launching.bat"

xcopy /s ".\spyke" "%INSTALL_DIR%"
if %errorlevel% neq 0 (
    echo Erreur inattendue lors de la copie des fichiers!
    exit /b
)
echo Fait.

echo Ne pas oublier de creer le raccourci de %INSTALL_DIR%\launching.bat

pause
