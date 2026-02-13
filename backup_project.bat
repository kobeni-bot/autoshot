@echo off
rem AutoShot Project Backup Script
rem Creates a complete backup of the project with all files and documentation

echo Creating AutoShot project backup...

rem Create backup directory with timestamp
set "backup_dir=autoshot_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
if not exist "%backup_dir%" mkdir "%backup_dir%"

rem Copy all project files
xcopy "autoshot" "%backup_dir%\autoshot" /E /I /Y
copy "pyproject.toml" "%backup_dir%" /Y
copy "README.md" "%backup_dir%" /Y
copy "PROJECT_DOCUMENTATION.md" "%backup_dir%" /Y
copy "test_autoshot.py" "%backup_dir%" /Y
copy "test_screenshot.py" "%backup_dir%" /Y

rem Create a zip archive
powershell Compress-Archive -Path "%backup_dir%" -DestinationPath "%backup_dir%.zip" -Force

echo Backup completed: %backup_dir%.zip
echo The backup contains all project files, documentation, and dependencies info.

pause