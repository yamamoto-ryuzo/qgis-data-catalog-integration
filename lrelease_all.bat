@echo off
setlocal
set LRELEASE="C:\Qt\linguist_6.9.1\lrelease.exe"
set I18NDIR=geo_import\i18n

rem Convert geo_import_*.ts translation files
for %%f in (%I18NDIR%\geo_import_*.ts) do (
    echo Converting %%f ...
    %LRELEASE% %%f
)
rem Legacy CKANBrowser_*.ts files (for backward compatibility)
for %%f in (%I18NDIR%\CKANBrowser_*.ts) do (
    echo Converting legacy %%f ...
    %LRELEASE% %%f
)
echo All .ts files converted to .qm.
pause
