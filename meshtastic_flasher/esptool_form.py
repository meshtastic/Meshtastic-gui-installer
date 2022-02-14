""" Run the esptool commands
"""

import re
import subprocess
import sys
import time
import traceback
import uuid
from collections import namedtuple

from PySide6.QtCore import (QObject, QRunnable, Qt, QThreadPool, QTimer,
                          Signal, Slot)
from PySide6.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit,
                             QProgressBar, QPushButton, QVBoxLayout, QWidget,
                             QDialog, QFormLayout, QLabel)

class WorkerSignals(QObject):
    """ Defines the signals available from a running worker thread. """
    result = Signal(str)  # Send back the output from the process as a string.
    finished = Signal()


class WorkerKilledException(Exception):
    pass

class SubProcessWorker(QRunnable):
    """ ProcessWorker worker thread
    Inherits from QRunnable to handle worker thread setup, signals and wrap-up.
    :param command: command to execute with `subprocess`.
    """
    def __init__(self, command):
        super().__init__()

        # Store constructor arguments (re-used for processing).
        self.signals = WorkerSignals()

        # The command to be executed.
        self.command = command

    # tag::workerRun[]
    @Slot()
    def run(self):
        """
        Initialize the runner function with passed args, kwargs.
        """
        with subprocess.Popen(
            self.command,
            bufsize=1,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True
        ) as proc:
            while proc.poll() is None:

                data = proc.stdout.readline()
                self.signals.result.emit(data)
        self.signals.finished.emit()
    # end::workerRun[]

class EsptoolForm(QDialog):
    def __init__(self, parent=None):
        super(EsptoolForm, self).__init__(parent)

        width = 500
        height = 400
        self.setMinimumSize(width, height)
        self.setWindowTitle("ESPTOOL output")

        layout = QVBoxLayout()

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        self.status_label = QLabel("running")
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # Thread runner
        self.threadpool = QThreadPool()

        self.finished = False

        #self.show()

    # tag::start[]
    def start(self):
        # Create a runner
        self.runner = SubProcessWorker(
            command="python3 dummy_script.py"
        )
        self.runner.signals.result.connect(self.result)
        self.runner.signals.finished.connect(self.do_finished)
        self.threadpool.start(self.runner)
    # end::start[]

    def do_finished(self):
        self.status_label.setText("done")
        self.finished = True
        print(f'self.finished:{self.finished}')

    def result(self, s):
        self.text.appendPlainText(s.strip())
