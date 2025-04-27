# -*- mode: python ; coding: utf-8 -*-
import os

# Configuración base CORREGIDA
project_root = os.getcwd()  # <- Usamos el directorio actual en vez de __file__
venv_rel_path = os.path.join('.venv', 'Lib', 'site-packages')
icon_rel_path = os.path.join('src', 'utils', 'assets', 'app_icon.ico')

block_cipher = None

a = Analysis(
    [os.path.join('src', 'main.py')],
    pathex=[
        os.path.join(project_root, 'src'),
        os.path.join(project_root, venv_rel_path)
    ],
    binaries=[],
    datas=[
        (icon_rel_path, 'utils/assets'),
        (os.path.join('src', 'utils', 'theme.json'), 'utils'),
        (os.path.join('src', 'utils', 'assets', '*'), 'utils/assets')
    ],
    hiddenimports=[
        'controllers',
        'models',
        'views',
        'utils',
        'services',
        'customtkinter',
        'yt_dlp',
        'PIL',
        'urllib3.contrib.emscripten',
        'curl_cffi',
        'brotli'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='AudioDownloaderPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    icon=os.path.join(project_root, icon_rel_path),
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AudioDownloaderPro',
)