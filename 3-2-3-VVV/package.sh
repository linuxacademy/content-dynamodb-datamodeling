#!/bin/sh

mkdir package
pip install --target ./package mutagen
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py
