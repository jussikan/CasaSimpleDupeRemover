#!/usr/bin/env bash

APP_NAME="CasaSimpleDupeRemover"

rm -rf "build/${APP_NAME}.app"
cp -Rp appskeleton "build/${APP_NAME}.app"

mkdir -p "build/${APP_NAME}.app/Contents/Resources/lib"
# TODO use just 'python3'.
python3.9 -m compileall lib
find lib/__pycache__ -type f -name '*.pyc' -exec mv {} "build/${APP_NAME}.app/Contents/Resources/lib" \;
cp main.py "build/${APP_NAME}.app/Contents/Resources/"

cp bin/{find-duplicates.sh,mark-duplicates.sh,delete-duplicates.sh} "build/${APP_NAME}.app/Contents/Resources/bin/"

