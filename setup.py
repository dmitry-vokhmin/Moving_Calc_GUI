from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

build_options = {'packages': ["os"], 'excludes': ["tkinter"],
                 "include_files": [("inv_images", "lib/inv_images")]}

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, target_name="Moving Calculator")
]

setup(name='Moving Calculator',
      version='1.0',
      description='',
      options={'build_exe': build_options},
      executables=executables)
