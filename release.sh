#!/bin/bash

pyinstaller -F --add-data "imgs/;." --add-data "fonts/;." --noconsole app.py

pyinstaller -F --add-data "imgs/;." --noconsole checker.py

# Create release folder
mkdir release

# Copy files to folder
cp -a fonts/. release/fonts/
cp -a imgs/. release/imgs/
cp dist/app.exe release/MusicBingo.exe
cp dist/checker.exe release/CardChecker.exe

# Remove build artifacts
rm -rf build/
rm -rf dist/
rm app.spec
