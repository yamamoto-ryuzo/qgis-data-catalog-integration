@echo off
setlocal
set LRELEASE="C:\Qt\linguist_6.9.1\lrelease.exe"
set I18NDIR=geo_import\i18n

rem Convert both legacy CKANBrowser_*.ts and new geo_import_*.ts
for %%f in (%I18NDIR%\geo_import_*.ts) do (
    echo Converting %%f ...
    %LRELEASE% %%f
)
for %%f in (%I18NDIR%\CKANBrowser_*.ts) do (
    echo Converting legacy %%f ...
    %LRELEASE% %%f
)
echo All .ts files converted to .qm.
pause
