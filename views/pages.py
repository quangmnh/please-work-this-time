from PyQt5 import QtCore, QtGui, QtWidgets
from utils1.snake_case import snake_case
from controller.MusicPlayer import Track


class PlaylistPage(QtWidgets.QWidget):
    def __init__(
            self,
            playlist_name,
            play_list_method,
            play_song_method,
            remove_method,
            go_to_lib_method,
            parent=None
    ):
        # Method is for when a song in the playlist is clicked
        super(PlaylistPage, self).__init__(parent)
        playlist_name = snake_case(playlist_name)
        self.playlist_name = playlist_name
        self.page_playlist_1 = QtWidgets.QWidget()
        self.page_playlist_1.setObjectName("page_" + playlist_name)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.page_playlist_1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.frame_playlist = QtWidgets.QFrame(self.page_playlist_1)
        self.frame_playlist.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_playlist.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_playlist.setObjectName("frame_playlist_" + playlist_name)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_playlist)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_playlist_name = QtWidgets.QLabel(self.frame_playlist)
        self.label_playlist_name.setText(self.playlist_name)
        self.label_playlist_name.setEnabled(True)
        self.label_playlist_name.setMinimumSize(QtCore.QSize(0, 60))
        self.label_playlist_name.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_playlist_name.setFont(font)
        self.label_playlist_name.setStyleSheet("color: #FFF;")
        self.label_playlist_name.setObjectName(
            "label_playlist_name_" + playlist_name)
        self.verticalLayout_11.addWidget(self.label_playlist_name)
        self.frame_playlist_buttons = QtWidgets.QFrame(self.frame_playlist)
        self.frame_playlist_buttons.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_playlist_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_playlist_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_playlist_buttons.setObjectName("frame_playlist_buttons")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(
            self.frame_playlist_buttons)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_playlist_play = QtWidgets.QPushButton(
            self.frame_playlist_buttons)
        self.btn_playlist_play.setText("Play")
        self.btn_playlist_play.setStyleSheet("QPushButton {\n"
                                             "    color: rgb(255,255,255);\n"
                                             "     background-color: rgb(35,35,35);\n"
                                             "    border: 0px solid;\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: rgb(85, 170, 255);\n"
                                             "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/play-circle.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_playlist_play.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_playlist_play.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_playlist_play.setIcon(icon)
        self.btn_playlist_play.setIconSize(QtCore.QSize(25, 25))
        self.btn_playlist_play.setStyleSheet("QPushButton {\n"
                                             "    color: rgb(255,255,255);\n"
                                             "    border: 0px solid;\n"
                                             "    border-radius: 25px;\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: rgb(85, 170, 255);\n"
                                             "}")
        self.btn_playlist_play.setText("")
        self.btn_playlist_play.setObjectName(
            "btn_playlist_play_" + playlist_name)
        self.horizontalLayout_2.addWidget(self.btn_playlist_play)
        self.btn_playlist_remove = QtWidgets.QPushButton(
            self.frame_playlist_buttons)
        self.btn_playlist_remove.setText("Remove playlist")
        self.btn_playlist_remove.setMinimumSize(QtCore.QSize(100, 50))
        self.btn_playlist_remove.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_playlist_remove.setStyleSheet("QPushButton {\n"
                                               "    color: rgb(255,255,255);\n"
                                               "     background-color: rgb(35,35,35);\n"
                                               "    border: 0px solid;\n"
                                               "}\n"
                                               "QPushButton:hover {\n"
                                               "    background-color: rgb(85, 170, 255);\n"
                                               "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/folder-minus.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_playlist_remove.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_playlist_remove.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_playlist_remove.setIcon(icon1)
        self.btn_playlist_remove.setIconSize(QtCore.QSize(25, 25))
        self.btn_playlist_remove.setStyleSheet("QPushButton {\n"
                                               "    color: rgb(255,255,255);\n"
                                               "    border: 0px solid;\n"
                                               "    border-radius: 25px;\n"
                                               "}\n"
                                               "QPushButton:hover {\n"
                                               "    background-color: rgb(85, 170, 255);\n"
                                               "}")
        self.btn_playlist_remove.setText("")
        self.btn_playlist_remove.setObjectName(
            "btn_playlist_remove_" + playlist_name)
        self.horizontalLayout_2.addWidget(self.btn_playlist_remove)
        self.btn_go_to_lib = QtWidgets.QPushButton(
            self.frame_playlist_buttons)
        self.btn_go_to_lib.setText("Go to library")
        self.btn_go_to_lib.setMinimumSize(QtCore.QSize(100, 50))
        self.btn_go_to_lib.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_go_to_lib.setStyleSheet("QPushButton {\n"
                                         "    color: rgb(255,255,255);\n"
                                         "     background-color: rgb(35,35,35);\n"
                                         "    border: 0px solid;\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(85, 170, 255);\n"
                                         "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/list.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_go_to_lib.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_go_to_lib.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_go_to_lib.setIcon(icon2)
        self.btn_go_to_lib.setIconSize(QtCore.QSize(25, 25))
        self.btn_go_to_lib.setStyleSheet("QPushButton {\n"
                                         "    color: rgb(255,255,255);\n"
                                         "    border: 0px solid;\n"
                                         "    border-radius: 25px;\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(85, 170, 255);\n"
                                         "}")
        self.btn_go_to_lib.setText("")
        self.btn_go_to_lib.setObjectName(
            "btn_go_to_lib_" + playlist_name)

        self.horizontalLayout_2.addWidget(self.btn_go_to_lib)
        self.verticalLayout_11.addWidget(
            self.frame_playlist_buttons, 0, QtCore.Qt.AlignLeft)
        self.listWidget_playlist_songs = QtWidgets.QListWidget(
            self.frame_playlist)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.listWidget_playlist_songs.setFont(font)
        self.listWidget_playlist_songs.setStyleSheet("color: #FFF;")
        self.listWidget_playlist_songs.setObjectName(
            "listWidget_playlist_songs_" + playlist_name)
        self.verticalLayout_11.addWidget(self.listWidget_playlist_songs)
        self.verticalLayout_13.addWidget(self.frame_playlist)

        # Connections
        self.listWidget_playlist_songs.clicked.connect(play_song_method)
        self.btn_playlist_play.clicked.connect(play_list_method)
        self.btn_playlist_remove.clicked.connect(remove_method)
        self.btn_go_to_lib.clicked.connect(go_to_lib_method)

        self.setLayout(self.verticalLayout_13)

        # self.row = QtWidgets.QHBoxLayout()

        # self.setStyleSheet("background-color: rgb(35,35,35);")

        # # Edit these fields to get correct song information
        # name = QtWidgets.QLabel(playlist_name)
        # ###################################################
        # name.setStyleSheet("color: white;")

        # self.row.addWidget(name)

        # self.play_btn = QtWidgets.QPushButton("Play")
        # self.remove_btn = QtWidgets.QPushButton("Remove")
        # self.play_btn.setStyleSheet("color: white;")
        # self.remove_btn.setStyleSheet("color: white;")

        # self.row.addWidget(self.play_btn)
        # self.row.addWidget(self.remove_btn)

        # self.setLayout(self.row)

        # self.play_btn.clicked.connect(play_list_method)
        # self.remove_btn.clicked.connect(remove_method)


class LoadingPage(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super(LoadingPage, self).__init__(parent)
        self.loading_page = QtWidgets.QWidget()
        self.loading_page.setObjectName("page_loading")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.loading_page)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
