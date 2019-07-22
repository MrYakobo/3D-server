#!/bin/sh

blender -b -P blender_script.py -- "$1" /dev/null | tail -n +4 | head -n -2