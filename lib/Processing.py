import asyncio
import threading
from typing import Callable, Coroutine


class Processing:
    # type here may differ per OS.
    self.async_loop: asyncio.unix_events._UnixSelectorEventLoop = None
    self.tasks: list = None
    self.fn: Coroutine = None
    self.script: str = None
    self.argv: list = None
    self.afterProcessing: Coroutine = None

    def __init__(self, async_loop: asyncio.unix_events._UnixSelectorEventLoop):
        self.async_loop = async_loop
        self.tasks = []

    def setProcessingAction(self, scriptOrFunction: str | Coroutine):
        if isinstance(scriptOrFunction, 'str'):
            self.script = scriptOrFunction
            self.fn = None
        elif isinstance(scriptOrFunction, 'Coroutine'):
            self.script = None
            self.fn = scriptOrFunction

    def setProcessingActionArguments(self, argv: list):
        self.argv = argv

    def setAfterProcessingFunction(self, fn: Coroutine):
        self.afterProcessing = fn

    async def runInShell(script: str) -> int:
        proc = await asyncio.create_subprocess_shell(' '.join([script, ' '.join(argv)]))
        foo = await proc.wait()
        print("type(foo):", type(foo))
        return foo

    # oli: async def initSubprocess
    async def executeProcessingFunction(self, returnAsap: bool):
        proc = await self.fn(*self.argv)
        return proc

    # oli: async def executeMockProcess
    async def initProcessing(self) -> asyncio.coroutine:
        task: asyncio.Task = None
        try:
            if self.script:
                task = asyncio.Task(self.runInShell(self.script))
            elif self.fn:
                task = asyncio.Task(self.executeProcessingFunction(False))
            else:
                return

            self.tasks.append(task)
        except asyncio.exceptions.CancelledError as cancelledError:
            print(cancelledError)
            return

        completed, pending = await asyncio.wait(tasks)
        await self.afterProcessing(completed, pending)

    def __asyncio_thread(self, async_loop: asyncio.unix_events._UnixSelectorEventLoop):
        mockPr = self.initProcessing()
        if mockPr is None:
            return
        print("type(mockPr):", type(mockPr))
        async_loop.run_until_complete(mockPr)

    # def __do_tasks(self):
    #     threading.Thread(target=self.__asyncio_thread, args=(self.async_loop,)).start()

    def execute(self):
        # self.__do_tasks()
        threading.Thread(target=self.__asyncio_thread, args=(self.async_loop,)).start()

    def clearTasks(self):
        self.tasks.clear()

    def cancelTasksInProgress(self):
        cancelCount = 0

        for task in self.tasks:
            if not task.done():
                try:
                    rv = task.cancel()
                    print("rv after task cancel:", rv)
                except asyncio.exceptions.CancelledError as cancelledError:
                    print("got CancelledError.")

                tasks.remove(task)  # is this wise always here?
                cancelCount = cancelCount + 1

        print(f"{cancelCount} tasks cancelled.")
