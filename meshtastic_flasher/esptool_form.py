""" Run the esptool commands
"""

import sys

import esptool

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QPlainTextEdit, QLabel, QPushButton


class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread."""
    data = Signal(str)
    status = Signal(str)
    finished = Signal()


class Worker(QRunnable):
    """ Worker thread
    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.
    """

    def __init__(self, update_only=False, port=None, device_file=None, system_info_file=None, bin_file=None, test=False):
        """constructor for the Worker class"""
        super().__init__()
        self.signals = WorkerSignals()

        self.update_only = update_only
        self.port = port
        self.device_file = device_file
        self.system_info_file = system_info_file
        self.bin_file = bin_file
        self.test = test # for unit testing (could not figure out how to patch)

    @Slot()
    def run(self):
        """Run the commands."""

        if not self.test:
            save_stdout = sys.stdout
            save_stderr = sys.stderr
            sys.stdout = self
            sys.stderr = self

        if self.update_only:
            print("Step 1/2 esp32 update only")
            self.signals.status.emit("Update step 1 of 2")
            command = ["--port", self.port, "write_flash", "0x10000", self.device_file]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            if not self.test:
                esptool.main(command)
            self.signals.status.emit("Update step 1 of 2 is done")

            print("Step 2/2 esp32 update only")
            command = ["--port", self.port, "erase_region", "0xe000", "0x2000"]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            if not self.test:
                esptool.main(command)
            self.signals.status.emit("Update step 2 of 2 is done")

        else:
            # do full flash
            print("Step 1/4 esp32 full")
            self.signals.status.emit("Full flash step 1 of 4")
            command = ["--port", self.port, "erase_flash"]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            if not self.test:
                esptool.main(command)
            self.signals.status.emit("Full flash step 1 of 4 is done")

            print("Step 2/4 esp32 full")
            command = ["--port", self.port, "write_flash", "0x1000", self.system_info_file]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            if not self.test:
                esptool.main(command)
            self.signals.status.emit("Full flash step 2 of 4 is done")

            print("Step 3/4 esp32 full")
            command = ["--port", self.port, "write_flash", "0x00390000", self.bin_file]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            if not self.test:
                esptool.main(command)
            self.signals.status.emit("Full flash step 3 of 4 is done")

            print("Step 4/4 esp32 full")
            command = ["--port", self.port, "write_flash", "0x10000", self.device_file]
            print(f"ESPTOOL Using command:{' '.join(command)}")
            if not self.test:
                esptool.main(command)
            self.signals.status.emit("Full flash step 4 of 4 is done")

        if not self.test:
            sys.stdout = save_stdout
            sys.stderr = save_stderr
            self.signals.finished.emit()


    def write(self, data):
        """Write the output that was intended for stdout/stderr to text box."""
        if data != '\n':
            self.signals.data.emit(data)

    def flush(self):
        """In case there is a flush() call on stdout or stderr."""

    def isatty(self):
        """needed for esptool"""
        return False


class EsptoolForm(QDialog):
    """Esptool form"""

    def __init__(self, parent=None):
        """constructor for the form"""

        super(EsptoolForm, self).__init__(parent)

        self.threadpool = QThreadPool()
        self.finished = False
        self.status = ""

        width = 600
        height = 500
        self.setMinimumSize(width, height)
        self.setWindowTitle("Flashing")

        layout = QVBoxLayout()

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("running")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch(1)

        self.ok_button = QPushButton("OK")
        self.ok_button.hide()
        bottom_layout.addWidget(self.ok_button)
        bottom_layout.addStretch(1)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.close_esptool_form)

    def close_esptool_form(self):
        """Test if works"""
        print('OK button was clicked in esptool form')
        self.close()

    def start(self, update_only=False, port=None, device_file=None, system_info_file=None, bin_file=None, test=False):
        """Create a thread to do the work."""
        # hide the button in case they are calling the esptool a subsequent time
        self.ok_button.hide()

        worker = Worker(update_only, port, device_file, system_info_file, bin_file, test)
        worker.signals.data.connect(self.receive_data)
        worker.signals.finished.connect(self.do_finished)
        worker.signals.status.connect(self.update_status)

        # Execute
        self.threadpool.start(worker)

    def update_status(self, data):
        """Update the status label"""
        self.status_label.setText(data)

    def do_finished(self):
        """When finished, update the label and let the user know it is done."""
        self.status_label.setText("")
        self.finished = True
        print(f'finished:{self.finished}')
        self.ok_button.show()

    def receive_data(self, data):
        """Update the text box from the stdout."""
        if data != '\n':
            self.text.appendPlainText(data.strip())
