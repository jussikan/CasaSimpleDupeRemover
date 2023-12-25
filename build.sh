#!/usr/bin/env bash

APP_NAME="CasaSimpleDupeRemover"

rm -rf "build/${APP_NAME}.app"
cp -Rp appskeleton "build/${APP_NAME}.app"

mkdir -p "build/${APP_NAME}.app/Contents/Resources/lib"
# TODO use just 'python3'.
# python3.9 -m compileall lib main.py
# find lib/__pycache__ -type f -name '*.pyc' -exec mv {} "build/${APP_NAME}.app/Contents/Resources/lib" \;
# mv __pycache__/main.*.pyc "build/${APP_NAME}.app/Contents/Resources/main.pyc"
find lib -type f -name '*.py' -exec cp {} "build/${APP_NAME}.app/Contents/Resources/lib" \;
cp main.py "build/${APP_NAME}.app/Contents/Resources/main.py"

cp bin/{find-duplicates.sh,mark-duplicates.sh,delete-duplicates.sh} "build/${APP_NAME}.app/Contents/Resources/bin/"
cp start.command "build/${APP_NAME}.app/Contents/MacOS/start"

find "build/${APP_NAME}.app" -type f -name '.DS_Store' -delete
rm "${APP_NAME}.zip" "${APP_NAME}_installer.zip"
cd build
zip -r -9 ../${APP_NAME}.zip "${APP_NAME}.app"
cd -
zip -r -9 "${APP_NAME}_installer.zip" "${APP_NAME}.zip" install.command
