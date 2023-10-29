import asyncio
import os
from pathlib import Path
import subprocess
from typing import List

from .phases import Phases
from .gui import GUI
from .processing import Processing

INITIAL_STATUS_LABEL_TEXT = "At your service."


def initPhases(app: 'Application'):
    app.phases = Phases()
    # these, or at least the script/command could be configurable.
    app.phases.createPhase("Find duplicates", "Finding duplicates", "Duplicates found", "find-duplicates.sh", "%{scrutinyDirectory}"),
    app.phases.createPhase("Mark duplicates", "Marking duplicates", "Duplicates marked", "mark-duplicates.sh"),
    app.phases.createPhase("Delete duplicates", "Deleting duplicates", "Duplicates deleted", "delete-duplicates.sh")


class Application:
    async_loop: asyncio.unix_events._UnixSelectorEventLoop = None
    phases: Phases = None
    gui: GUI = None
    # this for now for the macOS build.
    scriptDirectory: Path = None
    # workDirectory to be configurable, under user's home directory by default
    workDirectory: Path = None
    # to be set when user drops a directory onto the app window
    scrutinyDirectory: Path = None

    def __init__(self, async_loop: asyncio.unix_events._UnixSelectorEventLoop, argv: List[str]=[]):
        self.async_loop = async_loop
        # self.phases = Phases()
        # self.phases.createPhase("Find duplicates", "Finding duplicates", "Duplicates found")
        # etc
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

        self.scriptDirectory = Path(__file__).parent.parent.joinpath('bin')

        self.workDirectory = Path(os.path.expanduser('~'))

        self.processing = Processing(self.async_loop)
        self.processing.setAfterProcessingFunction(self.afterPhase)

    def setScrutinyDirectory(self, path: str):
        self.scrutinyDirectory = path

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
        phase = self.phases.getCurrent()
        self.gui.setStatusLabelText(phase.progressText)
        self.gui.setActionButtonState(GUI.state['DISABLED'])
        self.gui.setCancelButtonState(GUI.state['ACTIVE'])

        self.processing.setProcessingAction(str(Path(self.scriptDirectory, phase.shellScript)))

        if phase.argtpl and len(phase.argtpl) > 0:
            args = phase.argtpl.replace("%{scrutinyDirectory}", str(self.scrutinyDirectory))
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
