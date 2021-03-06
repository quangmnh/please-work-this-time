import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils1.snake_case import snake_case
from controller.MusicPlayer import TrackDatabase, Track


def QIcon_from_svg(svg_filepath, color='black'):
    img = QtGui.QPixmap(svg_filepath)
    qp = QtGui.QPainter(img)
    qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
    qp.fillRect(img.rect(), QtGui.QColor(color))
    qp.end()
    return QtGui.QIcon(img)


class LibrarySong(QtWidgets.QWidget):
    def __init__(
            self,
            song_info,
            on_play,
            on_remove,
            on_add_to_playlist,
            index,
            track_list: "list[Track]",
            parent=None):
        super(LibrarySong, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()

        # self.setStyleSheet("background-color: rgb(35,35,35);")

        # Edit these fields to get correct song information
        self.song_name = QtWidgets.QLabel(song_info['name'])
        self.song_artist = QtWidgets.QLabel(song_info['artist_name'])
        ###################################################
        self.song_name.setStyleSheet("color: white;")
        self.song_artist.setStyleSheet("color: white;")

        self.row.addWidget(self.song_name)
        self.row.addWidget(self.song_artist)

        self.play_btn = QtWidgets.QPushButton("Play")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/play.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.play_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.play_btn.setIcon(icon)
        self.play_btn.setStyleSheet("QPushButton {\n"
                                    "    color: rgb(255,255,255);\n"
                                    "    border: 0px solid;\n"
                                    "    border-radius: 20px;\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: rgb(85, 170, 255);\n"
                                    "}")
        self.play_btn.setText("")

        self.remove_btn = QtWidgets.QPushButton("Remove")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/x-circle.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.remove_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.remove_btn.setIcon(icon2)
        self.remove_btn.setStyleSheet("QPushButton {\n"
                                      "    color: rgb(255,255,255);\n"
                                      "    border: 0px solid;\n"
                                      "    border-radius: 20px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb(85, 170, 255);\n"
                                      "}")
        self.remove_btn.setText("")

        self.add_to_playlist_btn = QtWidgets.QPushButton("Add to playlist")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/folder-plus.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_to_playlist_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.add_to_playlist_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.add_to_playlist_btn.setIcon(icon3)
        self.add_to_playlist_btn.setStyleSheet("QPushButton {\n"
                                               "    color: rgb(255,255,255);\n"
                                               "    border: 0px solid;\n"
                                               "    border-radius: 20px;\n"
                                               "}\n"
                                               "QPushButton:hover {\n"
                                               "    background-color: rgb(85, 170, 255);\n"
                                               "}")
        self.add_to_playlist_btn.setText("")
        # self.play_btn.setStyleSheet("color: white;")
        # self.remove_btn.setStyleSheet("color: white;")
        # self.add_to_playlist_btn.setStyleSheet("color: white;")

        self.row.addWidget(self.play_btn)
        self.row.addWidget(self.add_to_playlist_btn)
        self.row.addWidget(self.remove_btn)

        self.setLayout(self.row)

        # CONNECTIONS
        self.play_btn.clicked.connect(
            lambda: on_play(int(index), track_list))
        self.remove_btn.clicked.connect(
            lambda: on_remove(int(index), "library_songs"))
        # self.add_to_playlist_btn.clicked.connect(lambda: on_add_to_playlist(0, int(index)))
        self.add_to_playlist_btn.clicked.connect(
            lambda: on_add_to_playlist(int(index)))


class BluetoothDevice(QtWidgets.QWidget):
    def __init__(self, device_info, on_connect_device, parent=None):
        super(BluetoothDevice, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()

        # Edit these fields to get correct device information
        self.device_name = QtWidgets.QLabel(device_info['name'])
        self.device_mac = QtWidgets.QLabel(device_info['mac'])
        ###################################################
        self.device_name.setStyleSheet("color: white;")
        self.device_mac.setStyleSheet("color: white;")

        self.row.addWidget(self.device_name)
        self.row.addWidget(self.device_mac)

        self.connect_btn = QtWidgets.QPushButton("Connect")
        self.connect_btn.setStyleSheet("color: white;")

        self.row.addWidget(self.connect_btn)

        self.setLayout(self.row)

        # CONNECTIONS
        self.connect_btn.clicked.connect(
            lambda: on_connect_device(device_info))


class PlaylistLabel(QtWidgets.QWidget):
    def __init__(self, playlist_name, on_open_playlist, parent=None):
        super(PlaylistLabel, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()
        self.playlist_name = snake_case(playlist_name)

        self.name = QtWidgets.QLabel(playlist_name)
        ###################################################
        self.name.setStyleSheet("color: white;")

        self.open_btn = QtWidgets.QPushButton("Open")
        self.open_btn.setStyleSheet("color: white;")

        self.row.addWidget(self.name)
        self.row.addWidget(self.open_btn)
        self.setLayout(self.row)

        # CONNECTIONS
        self.open_btn.clicked.connect(on_open_playlist)


class PlaylistSong(QtWidgets.QWidget):
    def __init__(
            self,
            song_info,
            on_play,
            on_remove,
            index,
            trackList: "list[Track]" = [],
            playlistName: str = "",
            parent=None
    ):
        super(PlaylistSong, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()

        # self.setStyleSheet("background-color: rgb(35,35,35);")

        # Edit these fields to get correct song information
        self.song_name = QtWidgets.QLabel(song_info['name'])
        self.song_artist = QtWidgets.QLabel(song_info['artist_name'])
        ###################################################
        self.song_name.setStyleSheet("color: white;")
        self.song_artist.setStyleSheet("color: white;")

        self.row.addWidget(self.song_name)
        self.row.addWidget(self.song_artist)

        self.play_btn = QtWidgets.QPushButton("Play")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/play.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.play_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.play_btn.setIcon(icon)
        self.play_btn.setStyleSheet("QPushButton {\n"
                                    "    color: rgb(255,255,255);\n"
                                    "    border: 0px solid;\n"
                                    "    border-radius: 20px;\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: rgb(85, 170, 255);\n"
                                    "}")
        self.play_btn.setText("")

        self.remove_btn = QtWidgets.QPushButton("Remove")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/x-circle.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.remove_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.remove_btn.setIcon(icon2)
        self.remove_btn.setStyleSheet("QPushButton {\n"
                                      "    color: rgb(255,255,255);\n"
                                      "    border: 0px solid;\n"
                                      "    border-radius: 20px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb(85, 170, 255);\n"
                                      "}")
        self.remove_btn.setText("")

        self.row.addWidget(self.play_btn)
        self.row.addWidget(self.remove_btn)

        self.setLayout(self.row)

        # CONNECTIONS
        self.play_btn.clicked.connect(lambda: on_play(int(index), trackList))
        self.remove_btn.clicked.connect(lambda: on_remove(
            int(index), playlistName=playlistName))


class Slider(QtWidgets.QSlider):
    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider,
                                         opt, QtWidgets.QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider,
                                         opt, QtWidgets.QStyle.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == QtCore.Qt.Horizontal else pr.y()
        return QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                                        sliderMax - sliderMin, opt.upsideDown)


class PlayIcon():
    def __init__(self, parent=None):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/icons/icons/play.svg"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)


class PauseIcon():
    def __init__(self, parent=None):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/icons/icons/pause.svg"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)


class RepeatIcon():
    def __init__(self, parent=None):
        self.icon = QIcon_from_svg(":/icons/icons/repeat.svg", color='white')


class RepeatEnabledIcon():
    def __init__(self, parent=None):
        self.icon = QIcon_from_svg(":/icons/icons/repeat.svg", color='#0d6efd')


class RepeatOneIcon():
    def __init__(self, parent=None):
        self.icon = QIcon_from_svg(
            ":/icons/icons/repeat-1.svg", color='#0d6efd')


class ShuffleEnabledIcon():
    def __init__(self, parent=None):
        self.icon = QIcon_from_svg(
            ":/icons/icons/shuffle.svg", color='#0d6efd')


class ShuffleIcon():
    def __init__(self, parent=None):
        self.icon = QIcon_from_svg(":/icons/icons/shuffle.svg", color='white')


class QtWaitingSpinner(QWidget):
    def __init__(self, parent, centerOnParent=True, disableParentWhenSpinning=False, modality=Qt.NonModal):
        super().__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        # WAS IN initialize()
        self._color = QColor(Qt.white)
        self._roundness = 100.0
        self._minimumTrailOpacity = 3.14159265358979323846
        self._trailFadePercentage = 80.0
        self._revolutionsPerSecond = 1.57079632679489661923
        self._numberOfLines = 20
        self._lineLength = 10
        self._lineWidth = 2
        self._innerRadius = 10
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()
        # END initialize()

        self.setWindowModality(modality)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, QPaintEvent):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(Qt.NoPen)
        for i in range(0, self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength,
                              self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(
                i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(distance, self._numberOfLines, self._trailFadePercentage,
                                          self._minimumTrailOpacity, self._color)
            painter.setBrush(color)
            rect = QRect(0, int(-self._lineWidth / 2),
                         int(self._lineLength), int(self._lineWidth))
            painter.drawRoundedRect(
                rect, self._roundness, self._roundness, Qt.RelativeSize)
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()

    def color(self):
        return self._color

    def roundness(self):
        return self._roundness

    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    def trailFadePercentage(self):
        return self._trailFadePercentage

    def revolutionsPersSecond(self):
        return self._revolutionsPerSecond

    def numberOfLines(self):
        return self._numberOfLines

    def lineLength(self):
        return self._lineLength

    def lineWidth(self):
        return self._lineWidth

    def innerRadius(self):
        return self._innerRadius

    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=Qt.black):
        self._color = QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self):
        size = int((self._innerRadius + self._lineLength) * 2)
        self.setFixedSize(size, size)

    def updateTimer(self):
        self._timer.setInterval(
            int(1000 / (self._numberOfLines * self._revolutionsPerSecond)))

    def updatePosition(self):
        if self.parentWidget() and self._centerOnParent:
            self.move(int(self.parentWidget().width() / 2 - self.width() / 2),
                      int(self.parentWidget().height() / 2 - self.height() / 2))

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput):
        color = QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(
            math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color
