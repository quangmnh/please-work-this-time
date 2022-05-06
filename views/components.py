from PyQt5 import QtCore, QtGui, QtWidgets

from utils1.snake_case import snake_case


class LibrarySong(QtWidgets.QWidget):
    def __init__(self, song_info, on_play, on_remove, on_add_to_playlist, parent=None):
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
        self.play_btn.clicked.connect(on_play)
        self.remove_btn.clicked.connect(on_remove)
        self.add_to_playlist_btn.clicked.connect(on_add_to_playlist)


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
