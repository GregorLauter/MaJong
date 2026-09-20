# Build on each target OS: uv run --extra desktop pyinstaller packaging/majong.spec
import sys
from pathlib import Path
from PyInstaller.utils.hooks import copy_metadata

root = Path(SPECPATH).parent
icon = root / "packaging" / ("majong.icns" if sys.platform == "darwin" else "majong.ico")
a = Analysis(
    [str(root / "packaging" / "desktop_entry.py")],
    pathex=[str(root / "src")],
    datas=[(str(root / "src" / "mahjong" / "assets"), "mahjong/assets"),
           (str(root / "SPEC.md"), "."),
           (str(root / "THIRD_PARTY_NOTICES.md"), ".")]
           + copy_metadata("PySide6") + copy_metadata("PySide6_Essentials")
           + copy_metadata("shiboken6"),
    hiddenimports=[],
    excludes=["PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "tkinter"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True, name="MaJong",
    console=False, icon=str(icon),
)
collection = COLLECT(exe, a.binaries, a.datas, name="MaJong")
if sys.platform == "darwin":
    app = BUNDLE(
        collection, name="MaJong.app", icon=str(icon),
        bundle_identifier="io.github.gregorlauter.majong",
        info_plist={"CFBundleShortVersionString": "0.1.0",
                    "NSHighResolutionCapable": True},
    )
