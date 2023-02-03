import sys
import re
import os.path
import subprocess
import zipfile

from setuptools import setup


BASEPATH = os.path.dirname(os.path.abspath(__file__))
JAR_FILE = 'scienceworld.jar'
JAR_PATH = os.path.join(BASEPATH, 'scienceworld', JAR_FILE)
# Extract ScienceWorld version from JAR file metadata
contents = zipfile.ZipFile(JAR_PATH).open('META-INF/MANIFEST.MF').read().decode('utf-8')
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

with open(os.path.join('scienceworld', 'version.py'), 'w') as f:
    f.write(f'__version__ = {VERSION!r}\n')

setup(version=VERSION)
