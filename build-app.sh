#!/usr/bin/env bash

python3.9 -m compileall lib
python3.9 cxfreeze_setup.py build
python3.9 cxfreeze_setup.py bdist_mac

# TODO pick these from the cxfreeze_setup.py.
APP_NAME="CasaSimpleDupeRemover"
VERSION="1.0"

cd "build/${APP_NAME}-${VERSION}.app/Contents/Resources/lib"
install_name_tool _tkinter.cpython-39-darwin.so -change @loader_path/../../../../opt/tcl-tk/lib/libtcl8.6.dylib @executable_path/lib/libtcl8.6.dylib
install_name_tool _tkinter.cpython-39-darwin.so -change @loader_path/../../../../opt/tcl-tk/lib/libtk8.6.dylib  @executable_path/lib/libtk8.6.dylib
codesign --sign - --force --preserve-metadata=entitlements,requirements,flags,runtime _tkinter.cpython-39-darwin.so
cd -

cp appskeleton/Contents/Resources/fi.casa.${APP_NAME}.plist "build/${APP_NAME}-${VERSION}.app/Contents/Resources/"
mkdir "build/${APP_NAME}-${VERSION}.app/Contents/Resources/bin"
cp appbin/*.sh "build/${APP_NAME}-${VERSION}.app/Contents/Resources/bin/"

# TODO component tests be ran at this point but not in this script

# TODO these to be moved to some distribution script
cd build
mv "${APP_NAME}-${VERSION}.app" "${APP_NAME}.app"
zip -r -9 "${APP_NAME}-${VERSION}.zip" "${APP_NAME}.app"
cd -
mv "build/${APP_NAME}-${VERSION}.zip" .
