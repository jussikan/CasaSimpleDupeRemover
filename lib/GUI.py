import tkinter

class GUI:
    # self.async_loop: asyncio.unix_events._UnixSelectorEventLoop = None
    self.window: tkinter.Tk = None
    self.statusLabel: tkinter.Label = None
    self.buttonAction: tkinter.Button = None
    self.buttonCancel: tkinter.Button = None

    # def __init__(self, async_loop: asyncio.unix_events._UnixSelectorEventLoop):
        # self.async_loop = async_loop
        #
    def __init__(self, windowTitleText: str):
        self.window = tkinter.Tk()
        # title could be configurable at build time
        self.window.title(windowTitleText)
        self.window.geometry('500x300')

        # self.statusLabel = tkinter.Label(self.window, text=initialLabelText)
        self.statusLabel = tkinter.Label(self.window)

        # self.buttonAction = tkinter.Button(self.window, text=initialActionButtonText)
        self.buttonAction = tkinter.Button(self.window)

        # text needs to be localizable
        self.buttonCancel = tkinter.Button(self.window, text="Cancel")

    def setStatusLabelText(self, text: str):
        self.statusLabel.configure(text=text)

    def setActionButtonState(self, state: str):
        self.buttonAction.configure(state=state)

    # mikä on fn:n tyyppi kun annetaan lambda, ja mikä kun annetaan funktio?
    def setActionButtonAction(self, fn):

    def setActionButtonText(self, text: str):
        self.buttonAction.configure(text=text)

    def run(self):
        # maybe do own calculation to get centered for real
        self.eval('tk::PlaceWindow . center')
        self.window.mainloop()
