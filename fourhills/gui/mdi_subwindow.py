import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5 import QtCore, QtGui, QtWidgets


def create_icon_by_color(color):
    pixmap = QtGui.QPixmap(1, 1)
    pixmap.fill(color)
    return QtGui.QIcon(pixmap)


class TitleProxyStyle(QtWidgets.QProxyStyle):
    def drawComplexControl(self, control, option, painter, widget=None):
        if control == QtWidgets.QStyle.CC_TitleBar:
            if hasattr(widget, "titleColor"):
                color = widget.titleColor
                if color.isValid():
                    option.palette.setBrush(
                        QtGui.QPalette.Highlight, QtGui.QColor(color)
                    )
            option.icon = create_icon_by_color(QtGui.QColor("transparent"))
        super(TitleProxyStyle, self).drawComplexControl(
            control, option, painter, widget
        )

class MdiSubWindow(QtWidgets.QMdiSubWindow):
    def __init__(self, parent=None, flags=QtCore.Qt.Widget):
        super(MdiSubWindow, self).__init__(parent, flags)
        self.setStyle(TitleProxyStyle(self.style()))
        self._titleColor = QtGui.QColor("#101116")


    @property
    def titleColor(self):
        return self._titleColor

    @titleColor.setter
    def titleColor(self, color):
        self._titleColor = color
        self.update()