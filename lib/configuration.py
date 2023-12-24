from pathlib import Path
import plistlib

from lib.phases import Phases

class Configuration:
    _scriptDirectory: Path = None

    # baseWorkDirectory to be configurable, under user's home directory by default
    _baseWorkDirectory: Path = None

    _phases: Phases = None

    def __init__(self):
        pass

    def loadFromFile(filePath: str) -> 'Configuration':
        pl = None

        print(filePath)
        with open(filePath, 'rb') as fp:
            pl = plistlib.load(fp, fmt=plistlib.FMT_XML)

        conf = Configuration()
        conf._scriptDirectory = Path(pl['scriptDirectory'])
        conf._baseWorkDirectory = Path(pl['baseWorkDirectory'])

        return conf


    @property
    def scriptDirectory(self) -> Path:
        return self._scriptDirectory

    @property
    def baseWorkDirectory(self) -> Path:
        return self._baseWorkDirectory

    @property
    def phases(self) -> Phases:
        return self._phases
