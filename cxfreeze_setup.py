from os import walk
from os.path import join
from cx_Freeze import setup, Executable

files = list(map(
    lambda e: join('lib/__pycache__', e),
    next(walk('./lib/__pycache__'), ([], None, []))[2]
))
files += ['main.py']

build_exe_options = {
    "include_files": files,
}

setup(
    name="CasaSimpleDupeRemover",
    version="1.0",
    description="My application description",
    options = {"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)],  # 'base=None' indicates a console application
)
