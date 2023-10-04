import asyncio
import os
from pathlib import Path

INITIAL_STATUS_LABEL_TEXT="At your service."


def __initPhases(app: Application):
    app.phases = Phases()
    # these, or at least the script/command could be configurable.
    app.phases.createPhase("Find duplicates", "Finding duplicates", "Duplicates found", "duperecorder.sh")    


class Application:
    self.async_loop: asyncio.unix_events._UnixSelectorEventLoop = None
    self.phases: Phases = None
    self.gui: GUI = None
    # this for now for the macOS build.
    self.scriptDirectory: Path = None
    # workDirectory to be configurable, under user's home directory by default
    self.workDirectory: Path = None
    # to be set when users drops a directory onto the app window
    self.scrutinyDirectory: Path = None

    def __init__(self, async_loop: asyncio.unix_events._UnixSelectorEventLoop):
        self.async_loop = async_loop
        # self.phases = Phases()
        # self.phases.createPhase("Find duplicates", "Finding duplicates", "Duplicates found")
        # etc
        __initPhases(self)
        self.phases.reset()

        app.gui = GUI('Duplicate file remover')
        app.gui.setStatusLabelText(INITIAL_STATUS_LABEL_TEXT)
        app.gui.setActionButtonText(self.phases.getCurrent().actionText)
        app.gui.setActionButtonAction(lambda: self.__onClickAction)

        self.scriptDirectory = Path(__file__).parent.joinpath('bin')

        self.workDirectory = Path(os.path.expanduser('~'))

        self.processing = Processing(self.async_loop)
        self.processing.setAfterProcessingFunction(self.afterPhase)

    # def __initPhases

    # nää async-hommat tuntuu vähän eri vastuulta kuin mitä tällä luokalla on..
    # joten jos lois jonku Processing-luokan niille.
    # def __asyncio_thread(async_loop: asyncio.unix_events._UnixSelectorEventLoop):
    #     mockPr = executeMockProcess()
    #     print("type(mockPr):", type(mockPr))
    #     async_loop.run_until_complete(mockPr)

    # def __do_tasks():
    #     threading.Thread(target=self.__asyncio_thread, args=(self.async_loop,)).start()

    # mitä parametrien tyypit on?
    async def afterPhase(completed, pending):
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
        self.gui.setActionButtonState(NORMAL)
        self.gui.setActionButtonText(phase.actionText)
        self.gui.setCancelButtonState(DISABLED)

    # mihin tätä tarvitaan?
    def __onCancelledAllTasks():
        # if self.phases.isAtFirstPhase():
        #   call gui to set label text to INITIAL_STATUS_LABEL_TEXT
        # else
        #   call gui to set label text to previous phase's actionText
        pass

    def __onClickAction():
        phase = self.phases.getCurrent()
        self.gui.setStatusLabelText(phase.progressText)
        self.gui.setActionButtonState(DISABLED)
        self.gui.setCancelButtonState(NORMAL)
        self.processing.setProcessingAction(Path(self.scriptDirectory, phase.shellScript))
        self.processing.setProcessingActionArguments([str(self.scrutinyDirectory)])

    def __onClickCancel():
        self.processing.cancelTasksInProgress()

        # voi olla et tätä joutuu säätää
        if self.phases.isAtFirstPhase():
            self.gui.setStatusLabelText(INITIAL_STATUS_LABEL_TEXT)
        else:
            self.gui.setStatusLabelText(self.phases.getCurrent().actionText)

    def run():
        self.gui.run()
