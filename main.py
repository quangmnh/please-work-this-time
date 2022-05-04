from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5 import QtCore, QtGui, QtWidgets
# GUI file
from views.ui_main import Ui_MainWindow

# Components
from views.components import BluetoothDevice, LibrarySong

# Pages
from views.pages import PlaylistPage

# Utils
from utils1.display_list_item import display_list_item

# Helper
from helper.playlist_page import *

import sys
import platform

# EXAMPLE DATA
############################################
playlist_no = 1


def increase_playlist_no():
    global playlist_no
    playlist_no += 1


bluetooth_devices = [
    {
        "name": "Hello",
        "mac": "FF:FF:FF:FF:FF"
    },
    {
        "name": "Boo",
        "mac": "EE:EE:EE:EE:EE"
    },
    {
        "name": "Hi",
        "mac": "DD:DD:DD:DD:DD"
    }]

library_songs = [
    {
        "name": "Hello",
        "artist_name": "Adele"
    },
    {
        "name": "September",
        "artist_name": "Earth, Wind & Fire"
    },
    {
        "name": "Viva La Vida",
        "artist_name": "Coldplay"
    }]
playlists = []
# END: EXAMPLE DATA ########################


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # PAGES
        ########################################################################

        # DASHBOARD PAGE
        self.ui.Btn_Dashboard.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_dashboard))

        # # LIBRARY PAGE
        # self.ui.Btn_Library.clicked.connect(
        #     lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_library))

        # EXAMPLE: LIBRARY PAGE WITH SONGS FETCH
        ########################################################################
        self.ui.Btn_Library.clicked.connect(
            lambda: (
                self.ui.Pages_Widget.setCurrentWidget(self.ui.page_library),
                display_list_item(
                    self.ui.listWidget_library_songs, [LibrarySong(song) for song in library_songs])
            ))
        ## END EXAMPLE: LIBRARY PAGE WITH SONGS FETCH ##########################

        # EMOTION RECOGNITION PAGE
        self.ui.Btn_menu_fer.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_emotion_recognition))

        # SETTINGS PAGE
        self.ui.Btn_Settings.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings))
        self.ui.Btn_menu_settings.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings))

        # SETTINGS: HAND GESTURE PAGE
        self.ui.Btn_settings_hand_gesture.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_hand_gesture))
        # SETTINGS: EMOTION PLAYLIST MAP PAGE
        self.ui.Btn_settings_emotion_map.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_emotion_playlist_map))
        # SETTINGS: BLUETOOTH PAGE
        self.ui.Btn_settings_bluetooth.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_bluetooth))

        ## END PAGES ###########################################################

        # EXAMPLE: BLUETOOTH DEVICE FETCH
        ########################################################################
        self.ui.btn_settings_bluetooth_scan_devices.clicked.connect(lambda: display_list_item(
            self.ui.listWidget_settings_bluetooth_devices, [BluetoothDevice(device) for device in bluetooth_devices]))
        ## END: EXAMPLE: BLUETOOTH DEVICE FETCH ################################

        # FUNCTIONALITY:
        ########################################################################
        ## Add playlist ####
        self.ui.Btn_Add_Playlist.clicked.connect(
            lambda: (
                create_playlist_dialog(
                    self.ui.Pages_Widget, self.ui.Pages_Widget, self.ui.listWidget_playlists)
            )
        )
        ## END : FUNCTIONALITY #################################################

        # MAIN WINDOW
        ########################################################################
        self.show()
        ## END MAIN WINDOW #####################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
