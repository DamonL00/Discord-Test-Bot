@echo off
echo ========================================
echo GitHub Push Automation Script
echo ========================================

set REPO_URL=https://github.com/DamonL00/Discord-Test-Bot.git
set COMMIT_MSG=Initial commit: Discord Kickoff League Bot

echo Starting GitHub push process...

REM Initialize Git repository if needed
if not exist .git (
    echo Initializing Git repository...
    git init
    if errorlevel 1 goto error
)

REM Check if user email is configured
git config --get user.email > nul 2>&1
if errorlevel 1 (
    echo Setting up Git identity...
    set /p EMAIL="Enter your GitHub email: "
    git config --global user.email "%EMAIL%"
    
    set /p USERNAME="Enter your GitHub username: "
    git config --global user.name "%USERNAME%"
)

REM Add remote if not exists
git remote -v | findstr "origin" > nul 2>&1
if errorlevel 1 (
    echo Adding remote repository...
    git remote add origin %REPO_URL%
)

REM Add all files to staging
echo Adding files to staging...
git add .
if errorlevel 1 goto error

REM Commit changes
echo Committing changes...
git commit -m "%COMMIT_MSG%"
if errorlevel 1 goto error

REM Push to GitHub
echo Pushing to GitHub...
echo You may be prompted for your GitHub credentials or token.
git push -u origin main
if errorlevel 1 (
    echo Push to 'main' branch failed, trying 'master' branch...
    git push -u origin master
    if errorlevel 1 goto pushfail
)

echo.
echo Success! Your code has been pushed to GitHub!
goto end

:error
echo.
echo An error occurred during the process.
goto end

:pushfail
echo.
echo Push failed. This might be due to authentication issues.
echo.
echo To authenticate:
echo 1. Generate a personal access token from GitHub:
echo    - Go to GitHub.com → Settings → Developer settings → Personal access tokens
echo    - Generate a new token with 'repo' permissions
echo    - Use this token as your password when prompted
echo.
echo 2. Or try using GitHub Desktop from https://desktop.github.com/

:end
echo.
echo Process completed.
pause 