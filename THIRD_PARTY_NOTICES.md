# Desktop dependencies

MaJong's desktop interface uses Qt for Python (PySide6) and Qt, distributed by
The Qt Company under their applicable open-source or commercial licenses.
These libraries are dynamically bundled by PyInstaller; their ownership and
licenses remain with their respective authors.

- Qt for Python: https://doc.qt.io/qtforpython-6/licenses.html
- Qt licenses: https://www.qt.io/licensing/open-source-lgpl-obligations
- Qt source and version archives: https://download.qt.io/official_releases/qt/
- PySide source: https://code.qt.io/cgit/pyside/pyside-setup.git/
- PyInstaller: https://pyinstaller.org/en/stable/license.html

Keep the bundled third-party license files when redistributing the application.
The application does not restrict modification or replacement of the bundled
Qt libraries for the purposes permitted by their licenses. The Python source,
build specification, and locked dependency versions are supplied in this
repository so the application can be rebuilt with compatible replacement libraries.
