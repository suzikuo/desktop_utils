# -*- mode: python ; coding: utf-8 -*-

icon_path = 'C:\\Users\\98027\\Desktop\\desktop_utils\\asserts\\icon\\kivy-icon-64.ico'
a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('kernel/', 'kernel'),
        ('asserts/', 'asserts'),
        ('apps/', 'apps'),
        ("config.json","."),
        ("utils.py","."),
        ("singleton.py","."),
        ("log.py",".")
    ],
    hiddenimports=[
        "logging.handlers",
        "paramiko",
        "tkinter",
        "tkinter.filedialog",
        "psutil",
        "queue",
        "tkinter.font",
        "tkinter.scrolledtext",
        "https.server",
        "json",
        "webbrowser",
        "multiprocessing",
        "win32gui"
    ],
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
    strip=False,  # Strip symbols
    upx=True,  # Enable UPX
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
    strip=True,  # Strip symbols
    upx=True,  # Enable UPX
    upx_exclude=[],
    name='run',
)
