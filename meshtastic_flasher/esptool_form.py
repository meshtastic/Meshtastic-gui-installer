""" Run the esptool commands
"""

import random
import sys
import time
import uuid

from PySide6.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QPlainTextEdit, QLabel


class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread."""
    data = Signal(str)
    finished = Signal()


def flush_then_wait():
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.5)

class Worker(QRunnable):
    """ Worker thread
    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.
    """

    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        # do stuff

        save_stdout = sys.stdout
        save_stderr = sys.stderr

        sys.stdout = self
        sys.stderr = self

        sys.stdout.write("Script stdout 1\n")
        sys.stdout.write("Script stdout 2\n")
        sys.stdout.write("Script stdout 3\n")
        flush_then_wait()

        sys.stdout.write("name=Martin\n")
        sys.stderr.write("Total time: 00:05:00\n")
        sys.stdout.write("Script stdout 4\n")
        sys.stdout.write("Script stdout 5\n")
        sys.stderr.write("Total complete: 0%\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:00:10\n")
        sys.stderr.write("Elapsed time: 00:00:50\n")
        sys.stderr.write("Total complete: 5%\n")
        sys.stdout.write("country=Nederland\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:01:10\n")
        sys.stderr.write("Total complete: 10%\n")
        sys.stdout.write("Script stdout 6\n")
        sys.stdout.write("Script stdout 7\n")
        sys.stdout.write("website=www.pythonguis.com\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:01:20\n")
        sys.stderr.write("Elapsed time: 00:02:50\n")
        sys.stderr.write("Total complete: 20%\n")
        sys.stdout.write("Script stdout 8\n")
        sys.stdout.write("Script stdout 9\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:02:90\n")
        sys.stderr.write("Total complete: 25%\n")
        sys.stderr.write("Elapsed time: 00:03:10\n")
        sys.stderr.write("Total complete: 30%\n")
        sys.stdout.write("Script stdout 10\n")
        sys.stdout.write("Script stdout 11\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:03:70\n")
        sys.stderr.write("Total complete: 35%\n")
        sys.stderr.write("Elapsed time: 00:03:90\n")
        sys.stderr.write("Total complete: 45%\n")
        sys.stdout.write("Script stdout 12\n")
        sys.stdout.write("Script stdout 13\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:04:10\n")
        sys.stderr.write("Total complete: 65%\n")
        sys.stderr.write("Elapsed time: 00:04:50\n")
        sys.stderr.write("Total complete: 75%\n")
        sys.stdout.write("Script stdout 14\n")
        sys.stdout.write("Script stdout 15\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:04:70\n")
        sys.stderr.write("Total complete: 80%\n")
        sys.stderr.write("Elapsed time: 00:04:90\n")
        sys.stderr.write("Total complete: 90%\n")
        sys.stdout.write("Script stdout 16\n")
        sys.stdout.write("Script stdout 17\n")
        flush_then_wait()

        sys.stderr.write("Elapsed time: 00:05:00\n")
        sys.stderr.write("Total complete: 100%\n")
        sys.stdout.write("Script stdout 18\n")
        sys.stdout.write("Script stdout 19\n")
        flush_then_wait()

        sys.stdout = save_stdout
        sys.stderr = save_stderr
        self.signals.finished.emit()


    def write(self, data):
        self.signals.data.emit(data)

    def flush(self):
        pass


class EsptoolForm(QDialog):
    def __init__(self, parent=None):
        super(EsptoolForm, self).__init__(parent)

        self.threadpool = QThreadPool()
        self.finished = False

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


    def start(self):
        worker = Worker()
        worker.signals.data.connect(self.receive_data)
        worker.signals.finished.connect(self.do_finished)

        # Execute
        self.threadpool.start(worker)

    def do_finished(self):
        self.status_label.setText("done")
        self.finished = True
        print(f'self.finished:{self.finished}')

    def receive_data(self, data):
        self.text.appendPlainText(data.strip())
