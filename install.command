#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# TODO check that homebrew is installed

brew install python3.9 tcl-tk python-tk@3.9
# or download https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz

cd "$SCRIPT_DIR"
unzip casadist.zip
mv CasaSimpleDupeRemover.app /Applications
