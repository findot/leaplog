#/usr/bin/env bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	LDPATH=linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
	LDPATH=osx
else
	echo "Unsupported operating system"
fi

PYTHONPATH=lib/$LDPATH:$PYTHONPATH python2 ./src/main.py
