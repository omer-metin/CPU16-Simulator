import time

from PyQt5 import QtCore, QtGui, QtWidgets

from common.types import BitString
from engine.hardware.components import InstructionMemory, Memory, Registers
from engine.software.mipsAssembler import MIPSAssembler
from gui.codeEditor import CodeEditor
from gui.simMainScreen_Ui import Ui_simMainWindow
from simProcessor import Processor


class SimMainScreen(QtWidgets.QMainWindow):

    # STATIC VARIABLES #
    _running = False
    _next = False
    _prev = False
    _backStack = []

    # DUNDERS #
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        ui = Ui_simMainWindow()
        ui.setupUi(self)
        self.initializeObjects()
        self.connectCallbacks()

    # PROPERTIES #

    # PUBLIC METHODS #
    def initializeObjects(self):
        self.assemblyEditor: CodeEditor = self.findChild(
            CodeEditor, "assemblyEditor")
        self.machineCodeViewer: CodeEditor = self.findChild(
            CodeEditor, "machineCodeViewer")

        memory_length = len(Memory._memory)*2
        self.memoryTableWidget: QtWidgets.QTableWidget = self.findChild(
            QtWidgets.QTableView, "memoryTableWidget")
        self.memoryTableWidget.setColumnCount(memory_length)

        self.stackTableWidget: QtWidgets.QTableWidget = self.findChild(
            QtWidgets.QTableView, "stackTableWidget")
        self.stackTableWidget.setColumnCount(memory_length)

        font = QtGui.QFont()
        font.setUnderline(True)
        for address in range(memory_length):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            item.setText("0x" + hex(address)[2:].upper())
            self.memoryTableWidget.setHorizontalHeaderItem(address, item)
            self.stackTableWidget.setHorizontalHeaderItem(
                memory_length - address - 1, item)
            self._updateMemoryCell(address, 0)

        self._bug = True

        self.registersTableWidget_1: QtWidgets.QTableWidget = self.findChild(
            QtWidgets.QTableWidget, "registersTableWidget_1")

        for reg_idx in range(len(Registers._init_registers)):
            self._updateRegister(reg_idx)

        self.delayLineEdit: QtWidgets.QLineEdit = self.findChild(
            QtWidgets.QLineEdit, "delayLineEdit")

    def connectCallbacks(self):
        self.assemblyEditor.textChanged.connect(
            self._assemblyEditor_textChanged)

        self.runButton: QtWidgets.QToolButton = self.findChild(
            QtWidgets.QToolButton, "runButton")
        self.runButton.clicked.connect(self._runButton_clicked)

        self.debugButton: QtWidgets.QToolButton = self.findChild(
            QtWidgets.QToolButton, "debugButton")
        self.debugButton.clicked.connect(self._debugButton_clicked)

        self.pauseButton: QtWidgets.QToolButton = self.findChild(
            QtWidgets.QToolButton, "pauseButton")
        self.pauseButton.clicked.connect(self._pauseButton_clicked)
        self.pauseButton.setDisabled(True)

        self.stopButton: QtWidgets.QToolButton = self.findChild(
            QtWidgets.QToolButton, "stopButton")
        self.stopButton.clicked.connect(self._stopButton_clicked)
        self.stopButton.setDisabled(True)

        self.previousButton: QtWidgets.QToolButton = self.findChild(
            QtWidgets.QToolButton, "previousButton")
        self.previousButton.clicked.connect(self._previousButton_clicked)
        self.previousButton.setDisabled(True)

        self.nextButton: QtWidgets.QToolButton = self.findChild(
            QtWidgets.QToolButton, "nextButton")
        self.nextButton.clicked.connect(self._nextButton_clicked)
        self.nextButton.setDisabled(True)

        self.actionOpen_File: QtWidgets.QAction = self.findChild(
            QtWidgets.QAction, "actionOpen_File")
        self.actionOpen_File.triggered.connect(self._actionOpen_File_triggered)

    # PRIVATE METHODS #
    def closeEvent(self, event):
        self._running = False
        return super().closeEvent(event)

    def _actionOpen_File_triggered(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName", "",
            "All Files (*);;Assembly Files (*.s)")
        if fname:
            with open(fname, 'r') as f:
                self.assemblyEditor.setPlainText(f.read())

    def _runButton_clicked(self):
        self._resetDebugger()
        self.pauseButton.setDisabled(False)
        self.stopButton.setDisabled(False)

        assembl_text = self.assemblyEditor.toPlainText()
        cursor: QtGui.QTextCursor = self.machineCodeViewer.textCursor()
        try:
            delay = float(self.delayLineEdit.text()) / 2
        except:
            delay = .5

        try:
            InstructionMemory.load_instructions(
                MIPSAssembler.assembly(assembl_text))
        except Exception as e:
            QtWidgets.QErrorMessage(self).showMessage(str(e))

        self._running = True
        old_pc = 0
        cursor.setPosition(0)
        self.machineCodeViewer.setTextCursor(cursor)
        step = Processor.processNext()
        while step is not None:
            if not self._running:
                break

            for address in range(2*len(Memory._memory)):
                QtWidgets.QApplication.processEvents()
                self._updateMemoryCell(address, 0)

            for _ in range(300):
                time.sleep(delay/300)
                QtWidgets.QApplication.processEvents()
            changed_regs, changed_mems = step
            for changed_reg in changed_regs:
                self._updateRegister(changed_reg[0])

            if InstructionMemory.PC-old_pc > 0:
                cursor.movePosition(QtGui.QTextCursor.Down,
                                    n=(InstructionMemory.PC-old_pc)//2)
            elif InstructionMemory.PC-old_pc < 0:
                cursor.movePosition(QtGui.QTextCursor.Up,
                                    n=abs(InstructionMemory.PC-old_pc)//2)
            self.machineCodeViewer.setTextCursor(cursor)

            old_pc = InstructionMemory.PC
            step = Processor.processNext()
        else:
            QtWidgets.QErrorMessage(self).showMessage("Done")

        self._running = False
        self.pauseButton.setDisabled(True)
        self.stopButton.setDisabled(True)

    def _debugButton_clicked(self):
        self._resetDebugger()
        self.stopButton.setDisabled(False)
        self.previousButton.setDisabled(False)
        self.nextButton.setDisabled(False)

        assembl_text = self.assemblyEditor.toPlainText()
        cursor: QtGui.QTextCursor = self.machineCodeViewer.textCursor()

        try:
            InstructionMemory.load_instructions(
                MIPSAssembler.assembly(assembl_text))
        except Exception as e:
            QtWidgets.QErrorMessage(self).showMessage(str(e))

        self._running = True
        old_pc = 0
        cursor.setPosition(0)
        self.machineCodeViewer.setTextCursor(cursor)
        step = 1
        while step is not None:
            if not self._running:
                break

            for address in range(2*len(Memory._memory)):
                QtWidgets.QApplication.processEvents()
                self._updateMemoryCell(address, 0)

            time.sleep(0.001)
            QtWidgets.QApplication.processEvents()
            if self._next:
                self._next = False
                if InstructionMemory.PC-old_pc > 0:
                    cursor.movePosition(QtGui.QTextCursor.Down,
                                        n=(InstructionMemory.PC-old_pc)//2)
                elif InstructionMemory.PC-old_pc < 0:
                    cursor.movePosition(QtGui.QTextCursor.Up,
                                        n=abs(InstructionMemory.PC-old_pc)//2)
                self.machineCodeViewer.setTextCursor(cursor)

                old_pc = InstructionMemory.PC
                step = Processor.processNext()
                if step is None:
                    continue
                changed_regs, changed_mems = step
                for changed_reg in changed_regs:
                    self._updateRegister(changed_reg[0])
                self._backStack.append((old_pc, InstructionMemory.PC, step))

            if self._prev:
                self._prev = False
                try:
                    prev_old_pc, prev_pc, prev_vals = self._backStack.pop()
                except IndexError as e:
                    old_pc = 0
                    InstructionMemory.PC = 0
                    continue
                if InstructionMemory.PC-prev_pc < 0:
                    cursor.movePosition(QtGui.QTextCursor.Down,
                                        n=abs(InstructionMemory.PC-prev_pc)//2)
                elif InstructionMemory.PC-prev_pc > 0:
                    cursor.movePosition(QtGui.QTextCursor.Up,
                                        n=(InstructionMemory.PC-prev_pc)//2)
                self.machineCodeViewer.setTextCursor(cursor)

                InstructionMemory.PC = prev_pc
                old_pc = prev_old_pc
                regs, mems = prev_vals
                for reg_idx, reg_val in regs:
                    self._reverseRegister(reg_idx, reg_val)
                for mem_adr, mem_val in mems:
                    self._reverseMemory(mem_adr, mem_val)

        else:
            QtWidgets.QErrorMessage(self).showMessage("Done")

        self._running = False
        self.stopButton.setDisabled(True)
        self.previousButton.setDisabled(True)
        self.nextButton.setDisabled(True)

    def _pauseButton_clicked(self):
        self._running = False

    def _stopButton_clicked(self):
        self._running = False

    def _previousButton_clicked(self):
        self._prev = True

    def _nextButton_clicked(self):
        self._next = True

    def _assemblyEditor_textChanged(self):
        assembly_lines = self.assemblyEditor.toPlainText()
        machineCodeViewer_text = ""
        try:
            for machine_code in MIPSAssembler.assembly(assembly_lines, True):
                machineCodeViewer_text += machine_code + "\n"
        except:
            return
        self.machineCodeViewer.setPlainText(machineCodeViewer_text)

    def _updateMemoryCell(self, address: int, c=1):
        memory_length = len(Memory._memory)*2
        dec_val = Memory.loadByte(address)
        bin_val = BitString(dec_val, length=8)

        item = QtWidgets.QTableWidgetItem(str(dec_val))
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.memoryTableWidget.setItem(0-c, address, item)
        item = QtWidgets.QTableWidgetItem(str(bin_val))
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.memoryTableWidget.setItem(1-c, address, item)

        item = QtWidgets.QTableWidgetItem(str(dec_val))
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.stackTableWidget.setItem(0+c, memory_length - address - 1, item)
        item = QtWidgets.QTableWidgetItem(str(bin_val))
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.stackTableWidget.setItem(1+c, memory_length - address - 1, item)

    def _updateRegister(self, reg_idx: int):
        item = QtWidgets.QTableWidgetItem(str("0x" + hex(
            Registers.getRegister(f"r{reg_idx}").value)[2:].upper()))
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.registersTableWidget_1.setItem(reg_idx, 0, item)
        item = QtWidgets.QTableWidgetItem(
            str(Registers.getRegister(f"r{reg_idx}").signedValue))
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.registersTableWidget_1.setItem(reg_idx, 1, item)
        item = QtWidgets.QTableWidgetItem(
            str(Registers.getRegister(f"r{reg_idx}").value))
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.registersTableWidget_1.setItem(reg_idx, 2, item)

    def _reverseMemory(self, address, val):
        Memory.storeByte(address, offset=0, value=val)
        self._updateMemoryCell(address)

    def _reverseRegister(self, reg_idx, val):
        if reg_idx < 16:
            Registers.getRegister(f"r{reg_idx}").setRegisterValue(val)
        elif reg_idx == 16:
            Registers.getRegister("hi").setRegisterValue(val)
        elif reg_idx == 33:
            Registers.getRegister("lo").setRegisterValue(val)
        else:
            Registers.getRegister(f"r{reg_idx-1}").setRegisterValue(val)
        self._updateRegister(reg_idx)

    def _resetDebugger(self):
        self.previousButton.setDisabled(True)
        self.nextButton.setDisabled(True)
        self.stopButton.setDisabled(True)
        self.pauseButton.setDisabled(True)
        Registers.resetRegisters()
        Memory.resetMemory()

        for address in range(2*len(Memory._memory)):
            QtWidgets.QApplication.processEvents()
            self._updateMemoryCell(address, 0)
        for idx in range(len(Registers._init_registers)):
            QtWidgets.QApplication.processEvents()
            self._updateRegister(idx)
