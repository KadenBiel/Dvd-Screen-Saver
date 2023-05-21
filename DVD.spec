# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['DVD.py'],
    pathex=[],
    binaries=[],
    datas=[('dvdFont.ttf','.'), ('save.dvd','.'), ('sprites/*.png','sprites')],
    hiddenimports=[],
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
    name='DVD',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
	icon='icon.ico'
)