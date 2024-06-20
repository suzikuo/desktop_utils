# -*- mode: python ; coding: utf-8 -*-

icon_path = 'C:\\Users\\98027\\Desktop\\desktop_utils\\asserts\\icon\\kivy-icon-64.ico'
a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[('kernel/', 'kernel'),('asserts/', 'asserts'),('apps/', 'apps'),("config.json","."),("utils.py","."),("singleton.py","."),("log.py",".")],
    hiddenimports=["logging.handlers","paramiko","tkinter","tkinter.filedialog","pystray","psutil","requests","queue","tkinter.font","tkinter.scrolledtext","PIL.Image","https","https.server"],
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
    exclude_binaries=True,
    name='MyBall',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path 
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run',
)
