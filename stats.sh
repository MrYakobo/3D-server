#!/bin/sh

if command -v jack_control > /dev/null; then
	jack_control start > /dev/null
fi

blender -b -P blender_script.py -- "$1"
