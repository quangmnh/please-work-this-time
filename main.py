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

        # LIBRARY PAGE
        self.ui.Btn_Library.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_library))

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

        # FUNCTIONALITY:
        ########################################################################
        ## Add playlist           ####
        self.ui.Btn_Add_Playlist.clicked.connect(
            self.on_create_playlist)
        ## Bluetooth settings     ####
        self.ui.btn_settings_bluetooth_scan_devices.clicked.connect(
            self.on_scan_bluetooth_devices)
        self.ui.btn_settings_bluetooth_disconnect.clicked.connect(
            self.on_disconnect_device)
        ## Hand gesture settings  ####
        self.ui.btn_settings_enable_hand_gesture.clicked.connect(
            self.on_hand_gesture)
        ## Emotion map settings   ####
        self.ui.comboBox_settings_emotion_playlist_map_happy.activated[str].connect(
            self.on_emotion_map_happy)
        self.ui.comboBox_settings_emotion_playlist_map_sad.activated[str].connect(
            self.on_emotion_map_sad)
        self.ui.comboBox_settings_emotion_playlist_map_angry.activated[str].connect(
            self.on_emotion_map_angry)
        self.ui.comboBox_settings_emotion_playlist_map_surprise.activated[str].connect(
            self.on_emotion_map_surprise)
        self.ui.comboBox_settings_emotion_playlist_map_neutral.activated[str].connect(
            self.on_emotion_map_neutral)
        ## Player                 ####
        self.ui.btn_player_navigator_playPause.clicked.connect(
            self.on_play_pause)
        self.ui.btn_player_navigator_forward.clicked.connect(
            self.on_next_song)
        self.ui.btn_player_navigator_previous.clicked.connect(
            self.on_previous_song)
        self.ui.btn_player_navigator_repeat.clicked.connect(
            self.on_repeat_mode)
        self.ui.btn_player_navigator_shuffle.clicked.connect(
            self.on_shuffle_mode)
        ## END : FUNCTIONALITY #################################################

        # MAIN WINDOW
        ########################################################################
        self.show()
        ## END MAIN WINDOW #####################################################

    # HANDLERS
    ########################################################################
    # Bluetooth
    def on_scan_bluetooth_devices(self):
        # TODO: Scan bluetooth devices
        display_list_item(self.ui.listWidget_settings_bluetooth_devices, [BluetoothDevice(
            device, on_connect_device=self.on_connect_device) for device in bluetooth_devices])

    def on_connect_device(self, device_info):
        # TODO: Connect to device
        print("Connecting to device: " + device_info['mac'])

    def on_disconnect_device(self):
        # TODO: Disconnect from bluetooth devices
        pass
    ### END: Bluetooth

    # Emotion Map
    def on_emotion_map_happy(self):
        # TODO: Assign playlist to happy emotion according to user's input
        pass

    def on_emotion_map_sad(self):
        # TODO: Assign playlist to sad emotion according to user's input
        pass

    def on_emotion_map_angry(self):
        # TODO: Assign playlist to angry emotion according to user's input
        pass

    def on_emotion_map_surprise(self):
        # TODO: Assign playlist to surprise emotion according to user's input
        pass

    def on_emotion_map_neutral(self):
        # TODO: Assign playlist to neutral emotion according to user's input
        pass
    # END : Emotion Map

    # Hand gesture
    def on_hand_gesture(self):
        # TODO: Enable and disable hand gesture script
        if self.ui.btn_settings_enable_hand_gesture.isChecked():
            print("Hand gesture enabled")
        else:
            print("Hand gesture disabled")
    # END: Hand gesture

    # Library
    def on_play_song(self):
        # TODO: Play song selected from library
        pass

    def on_remove_song(self):
        # TODO: Remove song from library
        pass

    def on_add_to_playlist(self):
        # TODO: Add song to playlist
        pass
    ### End : Library

    # Playlist
    # You can go to helper/playlist_page.py to see the declaration of the functions
    # like playing playlist or remove playlist page
    def on_create_playlist(self):
        create_playlist_dialog(
            self.ui.Pages_Widget, self.ui.Pages_Widget, self.ui.listWidget_playlists)
    ### End : Playlist

    # Player
    def on_play_pause(self):
        # TODO: Play/Pause
        pass

    def on_next_song(self):
        # TODO: Next song
        pass

    def on_previous_song(self):
        # TODO: Previous song
        pass

    def on_repeat_mode(self):
        # TODO: Change repeat mode
        pass

    def on_shuffle_mode(self):
        # TODO: Change shuffle mode
        pass
    ### End : Player

    # END : HANDLERS #######################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
