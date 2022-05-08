import os

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5 import QtCore, QtGui, QtWidgets
# GUI file
from views.ui_main import Ui_MainWindow

# Components
from views.components import (BluetoothDevice, LibrarySong, PlaylistLabel,
                              PlayIcon, PauseIcon, RepeatEnabledIcon,
                              RepeatIcon, RepeatOneIcon, ShuffleEnabledIcon, ShuffleIcon)

# Pages
from views.pages import PlaylistPage

# Utils
from utils1.display_list_item import display_list_item
from utils1.snake_case import snake_case

# Helper
# from helper.playlist_page import *

# Controllers
from controller.MusicPlayer import MusicPlayer, getDBFromJSON, getPlaylistList
from utils1.utils import *

import sys
import platform
import random

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

playlists = []
# END: EXAMPLE DATA ########################


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Icons
        self.play_icon = PlayIcon()
        self.pause_icon = PauseIcon()
        self.repeat_icon = RepeatIcon()
        # Set first for white color
        self.ui.btn_player_navigator_repeat.setIcon(self.repeat_icon.icon)
        self.repeat_one_icon = RepeatOneIcon()
        self.repeat_enabled = RepeatEnabledIcon()
        self.shuffle_icon = ShuffleIcon()
        self.shuffle_enabled = ShuffleEnabledIcon()
        # End : Icons

        self.media_player = MusicPlayer(
            playBack=trackDB.getTrackList()
        )

        # PAGES
        ########################################################################

        # DASHBOARD PAGE
        self.ui.Btn_Dashboard.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_dashboard))

        # LIBRARY PAGE
        self.ui.Btn_Library.clicked.connect(self.on_library_open)

        # EMOTION RECOGNITION PAGE
        self.ui.Btn_menu_fer.clicked.connect(self.on_emotion_recognition)

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

        # PLAYER
        # Track slider
        # Considering event for this
        self.ui.slider_player_navigator_progress_bar.sliderPressed.connect(
            self.on_set_position)
        # Volume slider
        self.ui.slider_player_volume.valueChanged.connect(self.on_set_volume)
        # END : PLAYER

        # PLAYER OBJECT
        # the callback will be called when the player emits the signal
        # Changing current postion of the progress bar
        self.media_player.player.positionChanged.connect(
            self.on_position_changed)
        # Changing the total duration of the progress bar
        self.media_player.player.durationChanged.connect(
            self.on_duration_changed)
        # Changing the button icon on state changes
        self.media_player.player.stateChanged.connect(
            self.on_mediastate_changed)
        # END : PLAYER OBJECT

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

    # Emotion recognition
    def on_emotion_recognition(self):
        # TODO: Enable the script and fetch the result
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_emotion_recognition)
    # END: Emotion recognition

    # Library
    def on_library_open(self):
        # TODO: Display all the songs once the library is opened
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_library)
        display_list_item(self.ui.listWidget_library_songs, [LibrarySong(
            song, self.on_play_song, self.on_remove_song, self.on_add_to_playlist, song.get('id')) for song in library_songs])

    def on_play_song(self, index: int):
        self.media_player.playSongAt(index)
        self.ui.change_label_player_track_in_navigator(
            self,
            trackName=self.media_player.playBack[index].getTrackName(),
            artistName=self.media_player.playBack[index].getArtistName()
        )

    def on_remove_song(self, index: int):
        self.media_player.deleteSong(index)
        new_playback = convert_from_track_list_to_list_dict(
            self.media_player.getPlaybackList())
        display_list_item(self.ui.listWidget_library_songs, [LibrarySong(
            song, self.on_play_song, self.on_remove_song, self.on_add_to_playlist, song.get('id')) for song in new_playback])

    def on_add_to_playlist(self):
        # TODO: Add song to playlist
        pass
    ### End : Library

    # Playlist
    def on_create_playlist(self):
        self.create_playlist_dialog(
            self.ui.Pages_Widget, self.ui.Pages_Widget, self.ui.listWidget_playlists)

    def on_playlist_song_play(self):
        # TODO : Play the song of the playlist
        pass

    def on_playlist_play(self):
        # TODO : Play the playlist
        pass

    def create_playlist_dialog(self, parent: QtWidgets.QWidget, page_widget: QtWidgets.QStackedWidget, playlist_list_widget: QtWidgets.QListWidget):
        dialog = QtWidgets.QInputDialog(parent)
        dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        dialog.setWindowTitle("Create Playlist")
        dialog.setLabelText('Playlist Name:')
        dialog.setStyleSheet("color: white; background-color: rgb(50,50,50);")
        ok = dialog.exec_()
        playlist_name = dialog.textValue()

        if ok and playlist_name:
            self.add_playlist_page(
                page_widget, playlist_name, playlist_list_widget)

    def add_playlist_page(self, page_widget: QtWidgets.QStackedWidget, playlist_name: str, playlist_list_widget: QtWidgets.QListWidget):
        """Add playlist page to page stack widget

        Args:
            page_widget (QtWidgets.QStackedWidget): Stack widget to add page to.
            playlist_name (str): Name of playlist to add.
            playlist_list_widget (QtWidgets.QListWidget): List widget to display all playlists.
        """
        playlist_label = PlaylistLabel(
            playlist_name, lambda: self.change_playlist_page(page_widget, playlist_name))

        # Add label to list widget
        entry = QtWidgets.QListWidgetItem(playlist_list_widget)
        playlist_list_widget.addItem(entry)
        entry.setSizeHint(playlist_label.minimumSizeHint())
        playlist_list_widget.setItemWidget(entry, playlist_label)

        playlist_page = PlaylistPage(playlist_name, self.on_playlist_play, self.on_playlist_song_play,
                                     lambda: self.remove_playlist_page(page_widget, playlist_name, playlist_list_widget, entry), self.on_library_open)
        # Add page to page stack
        page_widget.addWidget(playlist_page)

    def change_playlist_page(self, page_widget: QtWidgets.QStackedWidget, playlist_name: str):
        # TODO: Display the playlist songs here also
        num_page = page_widget.count()
        for i in range(num_page):
            w = page_widget.widget(i)
            if hasattr(w, "playlist_name") and w.playlist_name == snake_case(playlist_name):
                page_widget.setCurrentIndex(i)
                break

    def remove_playlist_page(self, page_widget: QtWidgets.QStackedWidget, playlist_name: str, playlist_list_widget: QtWidgets.QListWidget, playlist_label: QtWidgets.QListWidgetItem):
        num_page = page_widget.count()
        for i in range(num_page):
            w = page_widget.widget(i)
            if hasattr(w, "playlist_name") and w.playlist_name == snake_case(playlist_name):
                page_widget.removeWidget(w)
                page_widget.setCurrentIndex(0)
                break

        # Remove label from list widget
        playlist_list_widget.takeItem(playlist_list_widget.row(playlist_label))
    ### End : Playlist

    # Player
    # Play/Pause button
    def on_mediastate_changed(self, state):
        if self.media_player.player.state() == QMediaPlayer.PlayingState:
            self.ui.btn_player_navigator_playPause.setIcon(
                self.pause_icon.icon)
        else:
            self.ui.btn_player_navigator_playPause.setIcon(self.play_icon.icon)

        if self.media_player.getCurrPos() >= self.media_player.playBack[self.media_player.curr_playing].getTrackDuration():
            # Turn off repeat mode
            if self.media_player.repeatMode == 0:
                if self.media_player.curr_playing == len(self.media_player.playBack):
                    pass
                else:
                    self.on_next_song()
            # Repeat all tracks
            elif self.media_player.repeatMode == 1:
                self.on_next_song()
            # Repeat only one track
            else:
                self.on_play_song(self.media_player.curr_playing)

        if self.media_player.isShuffle:
            # TODO: change the Shuffle icon
            pass

    # Progress bar

    def on_position_changed(self, position):
        self.ui.slider_player_navigator_progress_bar.setValue(position)

    def on_duration_changed(self, duration):
        self.ui.slider_player_navigator_progress_bar.setRange(0, duration)

    def on_set_position(self):
        current_val = self.ui.slider_player_navigator_progress_bar.value()
        self.media_player.player.setPosition(current_val)

    def on_set_volume(self, volume):
        self.media_player.player.setVolume(volume)

    # Navigator
    def on_play_pause(self):
        self.media_player.togglePlayPause()

    def on_next_song(self):
        index = self.media_player.next()
        self.on_play_song(index)

    def on_previous_song(self):
        index = self.media_player.prev()
        self.on_play_song(index)

    def on_repeat_mode(self):
        self.media_player.changeRepeatMode()
        print(self.media_player.repeatMode)
        # Change icons
        if self.media_player.repeatMode == 1:
            self.ui.btn_player_navigator_repeat.setIcon(
                self.repeat_enabled.icon)
        elif self.media_player.repeatMode == 2:
            self.ui.btn_player_navigator_repeat.setIcon(
                self.repeat_one_icon.icon)
        else:
            self.ui.btn_player_navigator_repeat.setIcon(self.repeat_icon.icon)

    def on_shuffle_mode(self):
        self.media_player.toggleShuffleMode()
        # Change icons
        if self.media_player.isShuffle:
            self.ui.btn_player_navigator_shuffle.setIcon(
                self.shuffle_enabled.icon)
        else:
            self.ui.btn_player_navigator_shuffle.setIcon(
                self.shuffle_icon.icon)
    ### End : Player

    # END : HANDLERS #######################################################


if __name__ == "__main__":
    app = QApplication(sys.argv)

    trackDB = getDBFromJSON('sample.json')
    library_songs = convert_from_songDB_to_list_dict(trackDB)
    playlist_song = getPlaylistList('sample.json', trackDB)

    window = MainWindow()
    sys.exit(app.exec_())
