# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['PythonApplication1.py'],
    pathex=[],
    binaries=[],
    datas=[('CalcTimeForPoint.py', '.'), ('CalculateMidPoint.py', '.'), ('ExtractExif.py', '.'), ('HTMCalcTimeUI.py', '.'), ('MatchFiles.py', '.'), ('UIMatching.py', '.'), ('UIMiddling.py', '.'), ('visualInterface.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='my_program',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
