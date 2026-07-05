@echo off
title Git Push Utility
echo ======================================================================
echo                  Git Push Utility for NLP2SQL
echo ======================================================================
echo.

:: 1. Fix README.md folder issue if it exists as a folder
if exist README.md\ (
    echo [INFO] README.md exists as a directory. Deleting the directory...
    rmdir /s /q README.md
)
if not exist README.md (
    echo [INFO] Creating README.md file...
    echo # NLP2SQL > README.md
)

:: 2. Fix git history containing secrets (e.g. .env)
if exist .git (
    echo [WARNING] Re-initializing repository to clean any historical secrets...
    rmdir /s /q .git
)

echo [INFO] Initializing new Git repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to initialize git repository.
    pause
    exit /b 1
)

:: 3. Add files (respecting .gitignore which excludes .env)
echo [INFO] Adding files to stage...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to add files.
    pause
    exit /b 1
)

:: 4. Commit files
echo [INFO] Committing files...
git commit -m "Initialize project and add .gitignore"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to commit files.
    pause
    exit /b 1
)

:: 5. Rename branch to main
echo [INFO] Setting branch to main...
git branch -M main

:: 6. Configure remote origin
echo [INFO] Configuring remote origin...
git remote add origin https://github.com/Thomas09022006/NLP2SQL.git
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to configure remote origin.
    pause
    exit /b 1
)

:: 7. Push to remote
echo [INFO] Pushing code to GitHub...
echo [INFO] You might be prompted to authenticate with GitHub in your browser/credential manager.
git push -u origin main --force
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to push code to GitHub.
    echo Please make sure the repository exists and you have write permissions.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo [SUCCESS] Code successfully pushed to GitHub!
echo ======================================================================
echo.
pause
