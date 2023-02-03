import sys
import re
import os.path
import subprocess
import zipfile
from pathlib import Path

from setuptools import setup


BASEPATH = Path(__file__).resolve().parent

# Extract ScienceWorld version from JAR file metadata
JAR_PATH = BASEPATH / 'scienceworld' / 'scienceworld.jar'
with zipfile.ZipFile(JAR_PATH) as file:
    contents = file.open('META-INF/MANIFEST.MF').read().decode('utf-8')
VERSION = re.search(r'\bSpecification-Version: (.*)\b', contents).group(1)

# Based on https://github.com/microsoft/DeepSpeed/blob/28dfca8a13313b570e1ad145cf14476d8d5d8e16/setup.py#L170-L184
# Write out version/git info
git_hash_cmd = "git rev-parse --short HEAD"
try:
    result = subprocess.check_output(git_hash_cmd, shell=True)
    git_hash = result.decode('utf-8').strip()
    VERSION += f'+{git_hash}'
except subprocess.CalledProcessError:
    pass

# Dynamically create version file
with open(BASEPATH / 'scienceworld' / 'version.py', 'w') as f:
    f.write(f'__version__ = {VERSION!r}\n')

setup(version=VERSION)
