import asyncio
import datetime
import os
from pathlib import Path
import shutil
import subprocess
from typing import List


from lib.phases import Phases
from lib.gui import GUI
from lib.processing import Processing
from lib.configuration import Configuration

INITIAL_STATUS_LABEL_TEXT = "At your service."
PREFERENCE_LIST_FILENAME = 'fi.casa.CasaSimpleDupeRemover.plist'


def initPhases(app: 'Application'):
    app.phases = Phases()
    # these, or at least the script/command could be configurable.
    app.phases.createPhase("Scan for duplicates", "Scanning ..", "Scanning done", "find-duplicates.sh", "%{workDirectory} %{scrutinyDirectory}"),
    app.phases.createPhase("Mark duplicates", "Marking ..", "Marking done", "mark-duplicates.sh", "%{workDirectory}"),
    app.phases.createPhase("Delete duplicates", "Deleting ..", "Deletion done", "delete-duplicates.sh", "%{workDirectory}")


def getUserPreferencesPath() -> Path:
    return Path(os.path.expanduser('~')).joinpath('Library').joinpath('Application Support')


def loadConfig(home: Path) -> Configuration:
    config: Configuration = None
    userPlistFilePath = getUserPreferencesPath().joinpath(PREFERENCE_LIST_FILENAME)

    # in case user breaks the one in use,
    # this app could have a command for putting in place the default one.

    if userPlistFilePath.exists():
        config = Configuration.loadFromFile(userPlistFilePath)
    else:
        shutil.copyfile(home.joinpath(PREFERENCE_LIST_FILENAME), userPlistFilePath)
        config = Configuration.loadFromFile(userPlistFilePath)

    return config


def formWorkDirectoryName() -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    dt = now.strftime('%y%m%dT%H%M%S')
    return f"checksums-{dt}"


class Application:
    async_loop: asyncio.unix_events._UnixSelectorEventLoop = None
    phases: Phases = None
    gui: GUI = None

    # root of this application
    home: Path = None

    # this for now for the macOS build.

    workDirectory: Path = None

    # to be set when user drops a directory onto the app window
    scrutinyDirectory: Path = None

    config: Configuration = None

    def __init__(self, async_loop: asyncio.unix_events._UnixSelectorEventLoop, home, argv: List[str]=[]):
        self.async_loop = async_loop
        # self.phases = Phases()
        # self.phases.createPhase("Find duplicates", "Finding duplicates", "Duplicates found")
        # etc

        self.home = home
        self.config = loadConfig(self.home)

        initPhases(self)
        self.phases.reset()

        self.gui = GUI('Duplicate file remover')
        self.gui.setStatusLabelText(INITIAL_STATUS_LABEL_TEXT)
        phase = self.phases.getCurrent()

        self.gui.setActionButtonText(phase.actionText)
        self.gui.setActionButtonAction(self.__onClickAction)

        self.gui.setCancelButtonAction(self.__onClickCancel)
        self.gui.setCancelButtonState(GUI.state['DISABLED'])

        if len(argv) > 0 and os.path.isdir(argv[0]):
            self.setScrutinyDirectory(argv[0])
            self.gui.setDirectoryBoxText(argv[0])

        self.gui.setOnGetDirectoryPath(self.setScrutinyDirectory)



        self.processing = Processing(self.async_loop)
        self.processing.setAfterProcessingFunction(self.afterPhase)

    def setScrutinyDirectory(self, path: str):
        self.scrutinyDirectory = path

    def setWorkDirectory(self, path: str):
        self.workDirectory = path

    # nää async-hommat tuntuu vähän eri vastuulta kuin mitä tällä luokalla on..
    # joten jos lois jonku Processing-luokan niille.
    # def __asyncio_thread(async_loop: asyncio.unix_events._UnixSelectorEventLoop):
    #     mockPr = executeMockProcess()
    #     print("type(mockPr):", type(mockPr))
    #     async_loop.run_until_complete(mockPr)

    # def __do_tasks():
    #     threading.Thread(target=self.__asyncio_thread, args=(self.async_loop,)).start()

    # mitä parametrien tyypit on?
    async def afterPhase(self, completed, pending):
        results = [task.result() for task in completed]
        for result in results:
            if type(result) is subprocess.Popen:
                print("derp 1")
                print(result.poll())
            elif type(result) is asyncio.subprocess.Process:
                print("derp 2")
                await result.wait()
                print("rc from task:", result.returncode)
            else:
                print("derp 3")
                print("result from task:", result)
                print(type(result))

        self.processing.clearTasks()
        phase = self.phases.getCurrent()
        self.gui.setStatusLabelText(phase.completionText)
        phase = self.phases.advance()
        self.gui.setActionButtonState(GUI.state['NORMAL'])
        self.gui.setActionButtonText(phase.actionText)
        self.gui.setCancelButtonState(GUI.state['DISABLED'])

    # mihin tätä tarvitaan?
    def __onCancelledAllTasks():
        # if self.phases.isAtFirstPhase():
        #   call gui to set label text to INITIAL_STATUS_LABEL_TEXT
        # else
        #   call gui to set label text to previous phase's actionText
        pass

    def __onClickAction(self):
        if self.phases.isAtFirstPhase():
            self.setWorkDirectory(self.config.baseWorkDirectory.joinpath(formWorkDirectoryName()))

        phase = self.phases.getCurrent()
        self.gui.setStatusLabelText(phase.progressText)
        self.gui.setActionButtonState(GUI.state['DISABLED'])
        self.gui.setCancelButtonState(GUI.state['ACTIVE'])

        self.processing.setProcessingAction(str(Path(self.config.scriptDirectory, phase.shellScript)))

        if phase.argtpl and len(phase.argtpl) > 0:
            # NOTE could handle replacing all placeholders in separate function or class.
            args = phase.argtpl
            args = args.replace("%{workDirectory}", str(self.workDirectory))
            args = args.replace("%{scrutinyDirectory}", str(self.scrutinyDirectory))
            self.processing.setProcessingActionArguments([args])
        else:
            self.processing.setProcessingActionArguments([])

        self.processing.execute()

    def __onClickCancel(self):
        self.processing.cancelTasksInProgress()

        # voi olla et tätä joutuu säätää
        if self.phases.isAtFirstPhase():
            self.gui.setStatusLabelText(INITIAL_STATUS_LABEL_TEXT)
        else:
            self.gui.setStatusLabelText(self.phases.getCurrent().actionText)
        self.gui.setCancelButtonState(GUI.state['DISABLED'])
        self.gui.setActionButtonState(GUI.state['ACTIVE'])

    def run(self):
        self.gui.run()
