#!/usr/bin/env bash

python3.9 -m compileall lib
python3.9 cxfreeze_setup.py build > build.log 2>&1
python3.9 cxfreeze_setup.py bdist_mac > bdist_mac.log 2>&1

# TODO pick these from the cxfreeze_setup.py.
APP_NAME="CasaSimpleDupeRemover"
VERSION="1.0"

cd "build/${APP_NAME}-${VERSION}.app/Contents/Resources/lib"
echo -n > tuning.log
install_name_tool _tkinter.cpython-39-darwin.so -change @loader_path/../../../../opt/tcl-tk/lib/libtcl8.6.dylib @executable_path/lib/libtcl8.6.dylib >> tuning.log 2>&1
install_name_tool _tkinter.cpython-39-darwin.so -change @loader_path/../../../../opt/tcl-tk/lib/libtk8.6.dylib  @executable_path/lib/libtk8.6.dylib >> tuning.log 2>&1
codesign --sign - --force --preserve-metadata=entitlements,requirements,flags,runtime _tkinter.cpython-39-darwin.so >> tuning.log 2>&1
cd -

cp appskeleton/Contents/Resources/fi.casa.${APP_NAME}.plist "build/${APP_NAME}-${VERSION}.app/Contents/Resources/"
mkdir "build/${APP_NAME}-${VERSION}.app/Contents/Resources/bin"
cp appbin/*.sh "build/${APP_NAME}-${VERSION}.app/Contents/Resources/bin/"

# TODO component tests be ran at this point but not in this script

# Next: distribute.sh
