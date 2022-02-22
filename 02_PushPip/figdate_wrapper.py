import sys
import venv
import subprocess

from shutil import rmtree
from tempfile import mkdtemp

VENV_TEMPL = '{}/env'
PIP_TEMPL  = '{}/bin/pip'
PYTHON_TEMPL = '{}/bin/python'

INSTALL_FIGLET_ARGS = ['install', 'pyfiglet']
RUN_FIGDATE_ARGS = ['-m', 'figdate']


def install_figlet(venv_path):
    cmd_list = []
    cmd_list.append(PIP_TEMPL.format(venv_path))
    cmd_list += INSTALL_FIGLET_ARGS

    subprocess.run(cmd_list,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def run_figtate(venv_path, args=[]):
    cmd_list = []
    cmd_list.append(PYTHON_TEMPL.format(venv_path))
    cmd_list += RUN_FIGDATE_ARGS
    cmd_list += args

    subprocess.run(cmd_list)


def main():
    tmp_dir = mkdtemp()
    venv_path = VENV_TEMPL.format(tmp_dir)
    venv.create(venv_path, with_pip=True)

    install_figlet(venv_path)
    run_figtate(venv_path, sys.argv[1:])

    rmtree(tmp_dir)


if __name__ == '__main__':
    main()
