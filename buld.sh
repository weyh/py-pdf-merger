echo "Building..."

pyinstaller pdf_merger_ui.pyw -n "PDF Merger" --onefile --workpath="./build/tmp" --distpath="./build/bin" &&

mkdir -p './build/bin/lang' &&
cp "./lang/*" "./build/bin/lang" &&
cp "./LICENSE" "./build/bin/LICENSE" &&
cp "./README.md" "./build/bin/README.md" &&

mkdir -p './build/pkg' &&
zip './build/pkg/pdf_merger.zip' -r './build/bin' &&

echo "DONE!"
