$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$BundleRoot = Join-Path $ProjectRoot "release\macos\homework_nv_macos_bundle"
$AppRoot = Join-Path $BundleRoot "app"
$ModelSource = "D:\homework_yibai\_shared_runtime_assets\clip-vit-base-patch32-pytorch"

if (Test-Path $BundleRoot) {
    Remove-Item -Recurse -Force $BundleRoot
}

New-Item -ItemType Directory -Force -Path $AppRoot | Out-Null

Copy-Item "$ProjectRoot\README.md" $AppRoot
Copy-Item "$ProjectRoot\requirements.txt" $BundleRoot
Copy-Item "$ProjectRoot\weblog.md" $AppRoot
Copy-Item -Recurse "$ProjectRoot\src" $AppRoot
Copy-Item -Recurse "$ProjectRoot\data" $AppRoot
Copy-Item -Recurse "$ProjectRoot\artifacts" $AppRoot
Copy-Item -Recurse "$ProjectRoot\reports" $AppRoot
Copy-Item -Recurse "$ProjectRoot\docs" $AppRoot
Copy-Item -Recurse $ModelSource (Join-Path $AppRoot "models\clip-vit-base-patch32")

$LaunchScript = @'
#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$SCRIPT_DIR/app"
VENV_DIR="$SCRIPT_DIR/.venv"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required to run this bundle."
  exit 1
fi

if [ ! -x "$VENV_DIR/bin/python3" ]; then
  python3 -m venv "$VENV_DIR"
  "$VENV_DIR/bin/python3" -m pip install --upgrade pip
  "$VENV_DIR/bin/python3" -m pip install -r "$SCRIPT_DIR/requirements.txt"
fi

cd "$APP_DIR"
"$VENV_DIR/bin/python3" src/demo_app.py
'@

Set-Content -Path (Join-Path $BundleRoot "Launch_Visual_Style_Tool.command") -Value $LaunchScript -Encoding UTF8

Write-Host "macOS bundle prepared under $BundleRoot"
