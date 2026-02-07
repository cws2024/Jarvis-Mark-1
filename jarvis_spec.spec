# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# ============ DATA FILES ============
datas = []

# Add all Python files
import os
def collect_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                # Calculate relative path for destination
                rel_path = os.path.relpath(full_path, directory)
                py_files.append((full_path, os.path.join('jarvis', os.path.dirname(rel_path))))
    return py_files

# Add core files
datas.extend(collect_py_files('MAIN_JARVIS_SOFTWARE/src/core'))
datas.extend(collect_py_files('MAIN_JARVIS_SOFTWARE/src'))

# Add main files
datas.append(('jarvisgui.py', '.'))
datas.append(('jarvis.py', '.'))
datas.append(('launch_jarvis.py', '.'))

# Add config files if they exist
import glob
config_files = glob.glob('*.json') + glob.glob('*.log')
for f in config_files:
    datas.append((f, '.'))

# ============ HIDDEN IMPORTS ============
hiddenimports = [
    'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
    'pygame', 'pygame._sdl2', 'pygame.mixer', 'pygame.time',
    'psutil', 'numpy', 'pyautogui', 'pyperclip',
    'speech_recognition', 'pyttsx3', 'gtts',
    'yt_dlp', 'vlc',
    'requests', 'json', 'sys', 'os', 'threading',
    'queue', 'time', 'datetime', 'math', 'random',
    'pathlib', 'logging', 'subprocess', 'webbrowser',
    're', 'shutil', 'tempfile',
    'concurrent.futures', 'enum', 'collections',
    'dataclasses', 'typing', 'functools',
]

# Platform-specific imports
import platform
if platform.system() == 'Darwin':  # macOS
    hiddenimports.extend([
        'pyobjc', 'pyobjc_framework_Cocoa', 'pyobjc_framework_Quartz',
        'AppKit', 'Foundation',
    ])
elif platform.system() == 'Windows':
    hiddenimports.extend([
        'pywintypes', 'win32gui', 'win32con', 'win32process',
    ])

# ============ ANALYSIS ============
a = Analysis(
    ['jarvisgui.py'],
    pathex=['.', 'MAIN_JARVIS_SOFTWARE/src'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# ============ PYZ ============
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ============ EXE ============
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JARVIS_MARK_I',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Change to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='jarvis_icon.ico' if os.path.exists('jarvis_icon.ico') else None,
)

# ============ COLLECT ============
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='JARVIS_MARK_I',
)
