# -*- mode: python ; coding: utf-8 -*-
# Run from project root: pyinstaller installer/Abalone_Game.spec

a = Analysis(
    ['../driver.py'],
    pathex=['..'],
    binaries=[],
    datas=[
        ('../app/formations', 'app/formations'),
        ('../app/images', 'app/images'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='Abalone_Game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='../app/images/icon.ico',  # Uncomment after converting icon.png to icon.ico
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name='Abalone_Game',
)
