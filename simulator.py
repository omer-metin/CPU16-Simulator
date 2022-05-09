import time

from PyQt5 import QtWidgets

from gui.simMainScreen import SimMainScreen

app = QtWidgets.QApplication([])
simulator = SimMainScreen()
simulator.show()
app.exec_()
# ori $zero 14
# andc $zero $r1
# addc $rd $r1

# ori $zero 10
# andc $zero $r2
# addc $rd $r2

# subc $r2 $r1