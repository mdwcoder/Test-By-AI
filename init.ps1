$ErrorActionPreference = "Stop"

# Configuration
$ProjectDir = $PSScriptRoot
$VenvDir = Join-Path $ProjectDir ".venv"
$CliPath = Join-Path $ProjectDir "test_by_ai\cli.py"
$FunctionName = "test-by-ai"
$ProfilePath = $PROFILE.CurrentUserAllHosts

Write-Host "Detected Project Dir: $ProjectDir"

# Create .venv if not exists
if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating virtual environment..."
    python -m venv $VenvDir
} else {
    Write-Host "Virtual environment already exists."
}

# Install dependencies
Write-Host "Installing dependencies..."
$PipPath = Join-Path $VenvDir "Scripts\pip.exe"
& $PipPath install -r (Join-Path $ProjectDir "requirements.txt")

# Register Function in Profile
# Function definition
$FunctionDef = @"

# test-by-ai function
function $FunctionName {
    & "$VenvDir\Scripts\python.exe" "$CliPath" `$args
}
"@

# Check if profile exists
if (-not (Test-Path $ProfilePath)) {
    Write-Host "Profile not found, creating..."
    New-Item -ItemType File -Path $ProfilePath -Force | Out-Null
}

# Check content
$CurrentProfileContent = Get-Content $ProfilePath -Raw -ErrorAction SilentlyContinue
if ($CurrentProfileContent -match "function $FunctionName") {
    Write-Host "Function '$FunctionName' already exists in profile."
} else {
    Write-Host "Adding function to profile..."
    Add-Content -Path $ProfilePath -Value $FunctionDef
}

# Warning about Execution Policy
$ExPolicy = Get-ExecutionPolicy
if ($ExPolicy -eq "Restricted" -or $ExPolicy -eq "AllSigned") {
    Write-Warning "Your Execution Policy is '$ExPolicy'. You may need to run 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser' to load the profile."
}

Write-Host "--------------------------------------------------"
Write-Host "Success! Environment created and dependencies installed."
Write-Host "Function '$FunctionName' added to $ProfilePath"
Write-Host "Please restart your PowerShell session to use the command."
Write-Host "--------------------------------------------------"
