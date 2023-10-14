
class CanNotAdvanceError(Exception):
    def __init__(self):
        pass


class Phase:
    actionText: str = None
    progressText: str = None
    completionText: str = None
    shellScript: str = None

    def __init__(self, actionText: str, progressText: str, completionText: str, shellScript: str):
        self.actionText = actionText
        self.progressText = progressText
        self.completionText = completionText
        self.shellScript = shellScript


class Phases:
    collection = []
    current = None

    def __init__(self):
        pass

    def createPhase(self, actionText: str, progressText: str, completionText: str, shellScript: str):
        phase = Phase(actionText, progressText, completionText, shellScript)
        self.collection.append(phase)
        return phase

    def reset(self):
        if len(self.collection) > 0:
            self.current = 0

    def setCurrent(self, index: int):
        if len(self.collection) == 0:
            return

        if index >= 0 and index < len(self.collection):
            self.current = index

    def isAtFirstPhase(self) -> bool:
        return self.current == 0

    def advance(self) -> Phase:
        if self.current is None:
            return

        # if self.current >= 0:
        #     if self.current == len(self.collection) - 1:
        #         raise CanNotAdvanceError()
        #     else:
        #         self.current = self.current + 1

        # phase = self.getCurrent()
        # if (self.current + 1 <= len(self.collection)):
        #     self.current = self.current + 1
        # else:
        #     self.current = 0

        if (self.current + 1 < len(self.collection)):
            self.current = self.current + 1
        else:
            self.current = 0

        phase = self.collection[self.current]

        return phase

    def getFirstPhase(self) -> Phase:
        return self.collection[0]

    def getCurrent(self) -> Phase:
        return self.collection[self.current]

    def getLastPhase(self) -> Phase:
        return self.collection[ len(self.collection) - 1 ]
