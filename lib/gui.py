import tkinter

class GUI:
    window: tkinter.Tk = None
    statusLabel: tkinter.Label = None
    buttonAction: tkinter.Button = None
    buttonCancel: tkinter.Button = None
    state = {
        "ACTIVE": tkinter.ACTIVE,
        "NORMAL": tkinter.NORMAL,
        "DISABLED": tkinter.DISABLED
    }

    # def __init__(self, async_loop: asyncio.unix_events._UnixSelectorEventLoop):
        # self.async_loop = async_loop
        #
    def __init__(self, windowTitleText: str):
        self.window = tkinter.Tk()
        # title could be configurable at build time
        self.window.title(windowTitleText)
        self.window.geometry('200x300')
        self.window.configure(padx=20, pady=10)
        self.window.grid_columnconfigure(0, weight=1)

        # self.statusLabel = tkinter.Label(self.window, text=initialLabelText)
        self.statusLabel = tkinter.Label(self.window)
        self.statusLabel.grid(column=0, row=0)

        # self.buttonAction = tkinter.Button(self.window, text=initialActionButtonText)
        self.buttonAction = tkinter.Button(self.window, default=tkinter.ACTIVE, activeforeground='white')
        self.buttonAction.grid(column=0, row=1, sticky="ew")

        # text needs to be localizable
        self.buttonCancel = tkinter.Button(self.window, text="Cancel", default=tkinter.NORMAL)
        self.buttonCancel.grid(column=0, row=2, sticky="ew")

    def setStatusLabelText(self, text: str):
        self.statusLabel.configure(text=text)

    def setActionButtonState(self, state: str):
        self.buttonAction.configure(state=state)

    # mikä on fn:n tyyppi kun annetaan lambda, ja mikä kun annetaan funktio?
    def setActionButtonAction(self, fn):
        self.buttonAction.configure(command=fn)
        # self.window.bind('<Return>', lambda: fn)

    def setActionButtonText(self, text: str):
        self.buttonAction.configure(text=text)

    def setCancelButtonState(self, state: str):
        self.buttonCancel.configure(state=state)

    def setCancelButtonAction(self, fn):
        self.buttonCancel.configure(command=fn)

    def setCancelButtonText(self, text: str):
        self.buttonCancel.configure(text=text)

    def run(self):
        # maybe do own calculation to get centered for real
        self.window.eval('tk::PlaceWindow . center')
        self.window.mainloop()
