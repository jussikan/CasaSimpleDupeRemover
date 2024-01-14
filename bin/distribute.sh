#!/usr/bin/env bash

# TODO pick these from the cxfreeze_setup.py.
APP_NAME="CasaSimpleDupeRemover"
VERSION="1.0"

cd build
mv "${APP_NAME}-${VERSION}.app" "${APP_NAME}.app"
zip -r -9 "${APP_NAME}-${VERSION}.zip" "${APP_NAME}.app"
cd -
mkdir -p dist
mv "build/${APP_NAME}-${VERSION}.zip" dist/
