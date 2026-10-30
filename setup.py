import os
import setuptools
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

MODULE_NAME = "ok-script"

# Local builds must not query PyPI or change version according to network state.
VERSION_NUM = os.environ.get('OK_SCRIPT_BUILD_VERSION') or Path(__file__).with_name('VERSION').read_text().strip()

setuptools.setup(
    name=MODULE_NAME,
    version=VERSION_NUM,
    author="ok-oldking",
    author_email="firedcto@gmail.com",
    description="Automation with Computer Vision for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ok-oldking/ok-script",
    packages=setuptools.find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    license_files=['LICENSE.txt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
    install_requires=[
        'pywin32>=306; sys_platform == "win32"',
        'pyappify>=1.0.6',
        'PySide6-Fluent-Widgets>=1.8.3',
        'typing-extensions>=4.11.0',
        'requests>=2.32.3',
        'psutil>=6.0.0',
        'pydirectinput==1.0.4; sys_platform == "win32"',
        'pycaw==20240210; sys_platform == "win32"',
        'mouse==0.7.1; sys_platform == "win32"'
    ],
    entry_points={
        'console_scripts': [
            'ok=ok.cli:main',
        ],
    },
    python_requires='>=3.11',
    zip_safe=False,
)
