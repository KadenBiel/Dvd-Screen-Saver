# -*- mode: python -*-

block_cipher = None


a = Analysis(['DVD.py'],
             pathex=['C:\\Users\\kaden\\source\\repos\\DVD\\dvd builds'],
             binaries=[],
             datas=[('./sprites/w.png', './sprites'), ('./sprites/b.png', './sprites'), ('./sprites/g.png', './sprites'), ('./sprites/o.png', './sprites'), ('./sprites/p.png', './sprites'), ('./sprites/p2.png', './sprites'), ('./sprites/y.png', './sprites'), ('./dvdFont.ttf', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='DVD',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
