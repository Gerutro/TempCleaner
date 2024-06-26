@echo off
mkdir output
cd output
cls
"..\.venv\Scripts\pyinstaller.exe" --name TempCleaner --version-file ..\src\version_info.txt -i ..\src\recycle_bin.ico ..\Core\Main.py --onefile --clean --console
robocopy /MOV dist ..\..\TempCleaner
cd ..
del /F /S /Q output
for /d %%i in ("output") do rmdir /s /q "%%i"
exit