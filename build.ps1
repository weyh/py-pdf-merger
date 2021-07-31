Write-Output "Building..."

pyinstaller ./pdf_merger_ui.pyw -n "PDF Merger" --onefile --win-private-assemblies -i ".\icon.ico" --workpath="./build/tmp" --distpath="./build/bin"

New-Item -ItemType Directory -Force -Path "./build/bin/lang" > $null
Copy-Item -Path "./lang/*" -Destination "./build/bin/lang"
Copy-Item -Path "./icon.ico" -Destination "./build/bin/icon.ico"
Copy-Item -Path "./LICENSE" -Destination "./build/bin/LICENSE"
Copy-Item -Path "./README.md" -Destination "./build/bin/README.md"

New-Item -ItemType Directory -Force -Path "./build/pkg" > $null
Compress-Archive -Update -Path "./build/bin/*" -DestinationPath "./build/pkg/pdf_merger.zip"

Write-Output "Cleaning..."

Remove-Item ".\*.spec"
Remove-Item ".\__pycache__" -Force  -Recurse -ErrorAction SilentlyContinue

Write-Output "DONE!"
