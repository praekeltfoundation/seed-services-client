#!/bin/bash
VER="$1"

if [[ "x${VER}" = "x" ]]
then
    echo "Usage: $0 <version number>"
    echo " e.g. $0 0.1.0"
    exit 1
fi

function inplace_sed {
  # Note: we don't use sed -i -e ... because it isn't supported by FreeBSD
  # sed on OS X.
  suffix=".inplace.bak"
  sed -i"$suffix" -e "$1" "$2"
  rm "$2$suffix"
}

echo "${VER}" > VERSION
inplace_sed "s/^\(__version__[ ]*=[ ]*[\"']\)\(.*\)\([\"'].*\)/\1${VER}\3/" seed_services_client/__version__.py
