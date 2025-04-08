# GitHub Push Automation Script

# Repository URL
$repoUrl = "https://github.com/DamonL00/Discord-Test-Bot.git"

# Configuration - edit these if needed
$branchName = "main"
$commitMessage = "Initial commit: Discord Kickoff League Bot"

Write-Host "Starting GitHub Push Process..." -ForegroundColor Cyan

# Step 1: Initialize Git repo if not already initialized
if (-not (Test-Path -Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Green
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error initializing Git repository" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Configure Git user if not already configured
$userEmail = git config --get user.email
$userName = git config --get user.name

if (-not $userEmail) {
    $userEmail = Read-Host "Enter your GitHub email"
    git config --global user.email $userEmail
}

if (-not $userName) {
    $userName = Read-Host "Enter your GitHub username"
    git config --global user.name $userName
}

# Step 3: Add remote if not exists
$remoteExists = git remote -v | Select-String -Pattern "origin"
if (-not $remoteExists) {
    Write-Host "Adding remote repository..." -ForegroundColor Green
    git remote add origin $repoUrl
}

# Step 4: Add all files to staging
Write-Host "Adding files to staging..." -ForegroundColor Green
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error adding files to staging" -ForegroundColor Red
    exit 1
}

# Step 5: Commit changes
Write-Host "Committing changes..." -ForegroundColor Green
git commit -m $commitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error committing changes" -ForegroundColor Red
    exit 1
}

# Step 6: Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Green
Write-Host "You may be prompted for your GitHub credentials or token" -ForegroundColor Yellow

# Try to push using the default branch name
git push -u origin $branchName
$pushResult = $LASTEXITCODE

# If push fails with the default branch, try with master
if ($pushResult -ne 0 -and $branchName -eq "main") {
    Write-Host "Push to 'main' branch failed, trying 'master' branch..." -ForegroundColor Yellow
    git push -u origin master
    $pushResult = $LASTEXITCODE
}

# Report result
if ($pushResult -eq 0) {
    Write-Host "Success! Your code has been pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host @"
Push failed. This might be due to authentication issues.

To authenticate:
1. Try generating a personal access token from GitHub:
   - Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate a new token with 'repo' permissions
   - Use this token as your password when prompted

2. Or try using GitHub Desktop:
   - Download from https://desktop.github.com/
   - Clone your repository and push through the GUI
"@ -ForegroundColor Red
}

Write-Host "Process completed." -ForegroundColor Cyan 