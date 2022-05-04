from PyQt5 import QtCore, QtGui, QtWidgets

from utils1.snake_case import snake_case


class LibrarySong(QtWidgets.QWidget):
    def __init__(self, song_info, parent=None):
        super(LibrarySong, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()

        self.setStyleSheet("background-color: rgb(35,35,35);")

        # Edit these fields to get correct song information
        song_name = QtWidgets.QLabel(song_info['name'])
        song_artist = QtWidgets.QLabel(song_info['artist_name'])
        ###################################################
        song_name.setStyleSheet("color: white;")
        song_artist.setStyleSheet("color: white;")

        self.row.addWidget(song_name)
        self.row.addWidget(song_artist)

        play_btn = QtWidgets.QPushButton("Play")
        remove_btn = QtWidgets.QPushButton("Remove")
        add_to_playlist_btn = QtWidgets.QPushButton("Add to playlist")
        play_btn.setStyleSheet("color: white;")
        remove_btn.setStyleSheet("color: white;")
        add_to_playlist_btn.setStyleSheet("color: white;")

        self.row.addWidget(play_btn)
        self.row.addWidget(remove_btn)
        self.row.addWidget(add_to_playlist_btn)

        self.setLayout(self.row)


class BluetoothDevice(QtWidgets.QWidget):
    def __init__(self, device_info, parent=None):
        super(BluetoothDevice, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()

        # Edit these fields to get correct device information
        device_name = QtWidgets.QLabel(device_info['name'])
        device_mac = QtWidgets.QLabel(device_info['mac'])
        ###################################################
        device_name.setStyleSheet("color: white;")
        device_mac.setStyleSheet("color: white;")

        self.row.addWidget(device_name)
        self.row.addWidget(device_mac)

        connect_btn = QtWidgets.QPushButton("Connect")
        connect_btn.setStyleSheet("color: white;")

        self.row.addWidget(connect_btn)

        self.setLayout(self.row)


class PlaylistLabel(QtWidgets.QWidget):
    def __init__(self, playlist_name, open_playlist, parent=None):
        super(PlaylistLabel, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()
        self.playlist_name = snake_case(playlist_name)

        name = QtWidgets.QLabel(playlist_name)
        ###################################################
        name.setStyleSheet("color: white;")

        open_btn = QtWidgets.QPushButton("Open")
        open_btn.setStyleSheet("color: white;")

        open_btn.clicked.connect(lambda: open_playlist())

        self.row.addWidget(name)
        self.row.addWidget(open_btn)
        self.setLayout(self.row)
