#!/bin/bash
if [ $# -ne 1 ]
  then
    echo "usage:  packlambda.sh <sample name>"
    exit 1
fi
tmpdir=`mktemp -d`
cp -R ./samples/$1 $tmpdir
pushd $tmpdir/$1
pip install -t . -r requirements.txt --ignore-installed
zip -r $1 .
pushd
mv $tmpdir/$1/$1.zip .
