#!/usr/bin/env python3
# setup.py is the default file used by Distutils.
# As a developer you use this file for compiling/building the target installer. As a user this same file is used
# for installing the module.
#
# Usage
# Build the module for simulation: setup.py
# Build for simulation and install: setup.py install
# Build for the target: setup.py build --compile_for_target

import sys
import os
import shutil
import glob

if len(sys.argv) <= 1:
    sys.argv = ['setup.py', 'build']

from distutils.core import setup, Extension


sources = ['lvglmodule.c', 'lv_png.c', 'lodepng.c', 'noto_sans_cjk_18_2bpp.c']
# LVGL files
for path in 'lv_core', 'lv_draw', 'lv_font', 'lv_hal', 'lv_misc', 'lv_themes', 'lv_widgets':
    sources.extend(glob.glob('lvgl/src/' + path + '/*.c'))
# lv_driver files
for path in 'display', 'indev':
    sources.extend(glob.glob('lv_drivers/' + path + '/*.c'))
if os.name == 'nt':
    for path in '.', 'win32drv':
        sources.extend(glob.glob('lv_drivers/' + path + '/*.c'))

extra_compile_args = ["-I.", "-DLV_CONF_INCLUDE_SIMPLE"]
if os.name != 'nt':
    extra_compile_args.extend(["-g", "-Wno-unused-function", ])

# Do we want to compile for the target? (i.e. for the printer)
if "--compile_for_target" in sys.argv:
    libraries = []
    sys.argv.remove("--compile_for_target")
else:
    # By default, compile for simulation
    extra_compile_args.extend(["-DCOMPILE_FOR_SDL"])
    libraries = ["SDL2"]


module1 = Extension('lvgl',
                    sources = sources,
                    extra_compile_args = extra_compile_args,
                    libraries = libraries
                    )

dist = setup (name = 'lvgl',
       version = '0.1',
       description = 'lvgl bindings',
       ext_modules = [module1])

for output in dist.get_command_obj('build_ext').get_outputs():
    shutil.copy(output, '.')
