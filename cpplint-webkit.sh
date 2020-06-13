#!/bin/bash
set -e

FILES=${*: -1}

if [ "$FILES" = "$0" ]; then
  FILES="$CPPLINT_WEBKIT_FILES"
fi

check-webkit-style $CPPLINT_WEBKIT_ARGS $FILES 2>&1 | \
  sed 's;ERROR: ;;g' | \
  sed 's;[0-9]\: ;&warning:;' | \
  sed '/Suppressing further/d'
