#!/usr/bin/env bash


rm -rf CasaDupeRemover.app
cp -Rp appskeleton CasaDupeRemover.app

mkdir -p build/lib
python3.9 -m compileall lib
find lib/__pycache__ -type f -name '*.pyc' -exec cp {} build/lib

cp -R build/lib CasaDupeRemover.app/Contents/
