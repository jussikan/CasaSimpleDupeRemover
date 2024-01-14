import unittest

import asyncio
from pathlib import Path
import sys

from lib import application
from lib.application import Application
argv = sys.argv[1:]


class GeneralTest(unittest.TestCase):
    def test_FreshStartupWithPlistCreated(self):
        # assert plist file doesn't exist
        # NOTE maybe mock function application.getUserPreferencesPath so no need to worry about overwriting file in production.
        try:
            Application(asyncio.get_event_loop(), str(Path(__file__)))
        except:
             self.fail("Application.__init__ raised error unexpectedly")
        # assert plist file was created and its contents match with the original

    def test_RoutineStartup(self):
        try:
            Application(asyncio.get_event_loop(), str(Path(__file__)))
        except:
             self.fail("Application.__init__ raised error unexpectedly")

    def test_PathGivenOnCLIIsInsertedIntoDirectoryBox(self):
        path = Path(__file__).parent
        app = Application(asyncio.get_event_loop(), str(Path(__file__)), [str(path)])
        app.gui.directoryBox.xview("end")
        self.assertEqual(app.gui.entryText.get(), str(path))

    # TODO fix & finish
    def test_DirectoryCanBeDroppedOntoDirectoryBox(self):
        path = 'a'
        app = Application(asyncio.get_event_loop(), str(Path(__file__)))
        app.gui.directoryBox.event_generate('<<Drop>>', when='tail', data=path)
        self.assertEqual(app.gui.entryText.get(), path)

    def test_DirectoryCanBeScanned(self):
        path = Path('')
        # TODO have config file loaded from app's home directory.
        appHomeDir = Path(__file__)

        # TODO get contents of checksums directory

        app = Application(asyncio.get_event_loop(), str(appHomeDir), [str(path)])
        self.assertEqual(app.gui.buttonAction.cget('text'), "Scan for duplicates")
        self.assertEqual(app.gui.statusLabel, application.INITIAL_STATUS_LABEL_TEXT)

        app.gui.buttonAction.invoke()
        # need a mock script here, in another directory, and referenced in config
        self.assertEqual(app.gui.statusLabel, "Scanning ..")
        # sleep for a bit more than the script should run (or check processes if it's still running)
        # or check app.processing.tasks
        self.assertEqual(app.gui.statusLabel, "Scanning done")
        # TODO get contents of checksums directory again, assert that a new subdirectory was created, with checksums file inside.

        self.assertEqual(app.gui.buttonAction.cget('text'), "Mark duplicates")
        app.gui.buttonAction.invoke()
        self.assertEqual(app.gui.statusLabel, "Marking ..")
        # wait
        self.assertEqual(app.gui.statusLabel, "Marking done")

        self.assertEqual(app.gui.buttonAction.cget('text'), "Delete duplicates")
        app.gui.buttonAction.invoke()
        self.assertEqual(app.gui.statusLabel, "Deleting ..")
        # wait
        self.assertEqual(app.gui.statusLabel, "Deleting done")

    # TODO test Cancel button


if __name__ == '__main__':
    unittest.main()
