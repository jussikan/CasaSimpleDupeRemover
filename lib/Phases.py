
class CanNotAdvanceError(Error):
    def __init__(self):
        pass


class Phase:
    self.actionText: str = None
    self.progressText: str = None
    self.completionText: str = None
    self.shellScript: str = None

    def __init__(self, actionText: str, progressText: str, completionText: str, shellScript: str):
        self.actionText = actionText
        self.progressText = progressText
        self.completionText = completionText
        self.shellScript = shellScript


class Phases:
    self.collection = []
    self.current = None

    def __init__(self):
        pass

    def createPhase(actionText: str, progressText: str, completionText: str):
        phase = Phase(actionText, progressText, completionText)
        self.collection.append(phase)
        return phase

    def reset():
        if len(self.collection) > 0:
            self.current = 0

    def setCurrent(index: int):
        if len(self.collection) == 0:
            return

        if index >= 0 and index < len(self.collection):
            self.current = index

    def isAtFirstPhase() -> bool:
        return self.current == 0

    def advance() -> Phase:
        if self.current is None:
            return

        if self.current >= 0:
            if self.current == len(self.collection) - 1:
                raise CanNotAdvanceError()
            else:
                self.current = self.current + 1

        return self.getCurrent()

    def getFirstPhase() -> Phase:
        return self.collection[0]

    def getCurrent() -> Phase:
        return self.collection[self.current]

    def getLastPhase() -> Phase:
        return self.collection[ len(self.collection) - 1 ]
