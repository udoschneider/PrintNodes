import subprocess
import sys
import importlib.util

from . import config


def addPip(strLibrary, reinstall=False):
    if importlib.util.find_spec(strLibrary) is None:
        # Ensure pip is installed
        try:
            subprocess.check_call(
                [sys.executable, "-m", "ensurepip", "--upgrade"])
        except subprocess.CalledProcessError as e:
            print(f'Caught CalledProcessError while trying to ensure pip is installed')
            print(f'  Exception: {e}')
            print(f'  {sys.executable}')
            # return False
            pass

        mode = "--upgrade"
        if reinstall:
            mode = "--force-reinstall"

        sub = subprocess.run(
            [sys.executable, "-m", "pip", "install", mode, strLibrary])
        if sub.returncode != 0:
            return False
        return True


def addPackages():
    for strPackage in config.PIP_PACKAGES:
        addPip(strPackage)
