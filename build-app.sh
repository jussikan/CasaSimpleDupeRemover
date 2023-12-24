#!/usr/bin/env bash

python3.9 cxfreeze_setup.py build
python3.9 cxfreeze_setup.py bdist_mac

cd build/CasaSimpleDupeRemover-1.0.app/Contents/Resources/lib
install_name_tool _tkinter.cpython-39-darwin.so -change @loader_path/../../../../opt/tcl-tk/lib/libtcl8.6.dylib @executable_path/lib/libtcl8.6.dylib
install_name_tool _tkinter.cpython-39-darwin.so -change @loader_path/../../../../opt/tcl-tk/lib/libtk8.6.dylib  @executable_path/lib/libtk8.6.dylib
codesign --sign - --force --preserve-metadata=entitlements,requirements,flags,runtime _tkinter.cpython-39-darwin.so
cd -
