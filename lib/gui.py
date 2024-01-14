import os
import re
import tkinter
import typing
from tkinter import ttk
from tkinterdnd2 import DND_ALL, DND_TEXT, DND_FILES, TkinterDnD

class GUI:
    window: tkinter.Tk = None
    entryText: tkinter.StringVar = None
    directoryBox: tkinter.Label = None
    scroller = ttk.Scrollbar = None
    statusLabel: tkinter.Label = None
    buttonAction: tkinter.Button = None
    buttonCancel: tkinter.Button = None
    onGotDirectoryPath: typing.Callable = None
    state = {
        "ACTIVE": tkinter.ACTIVE,
        "NORMAL": tkinter.NORMAL,
        "DISABLED": tkinter.DISABLED
    }

    def __init__(self, windowTitleText: str):
        self.window = TkinterDnD.Tk()
        # title could be configurable at build time
        self.window.title(windowTitleText)
        self.window.geometry('200x300')
        self.window.configure(padx=20, pady=10)
        self.window.grid_columnconfigure(0, weight=1)

        self.entryText = tkinter.StringVar()
        self.scroller = tkinter.Scrollbar(self.window, orient=tkinter.HORIZONTAL)
        self.directoryBox = tkinter.Entry(self.window, state='readonly', textvariable=self.entryText, justify=tkinter.CENTER)
        self.directoryBox.configure(relief="solid", xscrollcommand=self.scroller.set)
        self.entryText.set("Drop folder here")
        self.directoryBox.drop_target_register(DND_FILES)
        self.directoryBox.dnd_bind("<<Drop>>", lambda event: self.onDirectoryDrop(event))
        self.directoryBox.grid(column=0, row=0, sticky="ew")

        self.scroller.configure(command=self.directoryBox.xview)

        # self.statusLabel = tkinter.Label(self.window, text=initialLabelText)
        self.statusLabel = tkinter.Label(self.window)
        self.statusLabel.grid(column=0, row=2)

        # self.buttonAction = tkinter.Button(self.window, text=initialActionButtonText)
        self.buttonAction = tkinter.Button(self.window, default=tkinter.ACTIVE, activeforeground='white')
        self.buttonAction.grid(column=0, row=3, sticky="ew")

        # text needs to be localizable
        self.buttonCancel = tkinter.Button(self.window, text="Cancel", default=tkinter.NORMAL)
        self.buttonCancel.grid(column=0, row=4, sticky="ew")

    def setDirectoryBoxText(self, path: str):
        self.entryText.set(path)
        self.directoryBox.xview("end")

    def onDirectoryDrop(self, event: TkinterDnD.DnDEvent):
        if len(event.data) > 0:
            path = re.sub(r"}$", "", re.sub(r"^{", "", event.data))
            if os.path.isdir(path):
                self.scroller.grid(column=0, row=1, sticky="ew")
                self.entryText.set(path)
                self.directoryBox.xview("end")
                self.onGotDirectoryPath(self.entryText.get())  # TODO TEST

    # TODO TEST
    def setOnGetDirectoryPath(self, fn: typing.Callable):
        self.onGotDirectoryPath = fn

    def setStatusLabelText(self, text: str):
        self.statusLabel.configure(text=text)

    def setActionButtonState(self, state: str):
        self.buttonAction.configure(state=state)

    def setActionButtonAction(self, fn):
        self.buttonAction.configure(command=fn)

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
