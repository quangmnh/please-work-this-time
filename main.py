import json
import os

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtCore import (QObject, QThread, pyqtSignal)
from PyQt5 import QtCore, QtGui, QtWidgets
# GUI file
from views.ui_main import Ui_MainWindow

# Components
from views.components import (BluetoothDevice, LibrarySong, PlaylistLabel, PlaylistSong,
                              PlayIcon, PauseIcon, RepeatEnabledIcon,
                              RepeatIcon, RepeatOneIcon, ShuffleEnabledIcon, ShuffleIcon, QtWaitingSpinner)

# Pages
from views.pages import PlaylistPage

# Utils
from utils1.display_list_item import display_list_item
from utils1.snake_case import snake_case

# Helper
# from helper.playlist_page import *

# Controllers
from controller.MusicPlayer import MusicPlayer, getDBFromJSON, getPlaylistList, PlayList
from controller.scan_usb import auto_detect_music_in_usb
from controller.create_json import updateTrackDatabaseFromFolderToJsonFile, updateEmotionPlaylistJson
from utils1.utils import *

import sys
import platform
import random
from time import time

from controller.model_manager import *
from controller.blutooth_controller import *

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

# END: EXAMPLE DATA ########################


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, long_run_method, parent: None) -> None:
        super().__init__(parent)
        self.method = long_run_method

    def run(self):
        self.method()
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # comment this section for windows testing and set these to None, fuk u all windows users
        self.camera = CameraManagement()
        self.face_recognition = ONNXClassifierWrapper2(
            "controller/new_caffe.trt", [1, 1, 200, 7], 0.5, target_dtype=np.float32)
        self.emotion_recognition = ONNXClassifierWrapper(
            "controller/new_model.trt", [1, 5], target_dtype=np.float32)
        self.bluetooth = BluetoothController(10)

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

        # Add spinner to loading screen
        self.loading_orb = QtWaitingSpinner(
            self.ui.frame_emotion_recognition_loading_orb)
        self.loading_orb.start()
        # End : Add spinner

        self.media_player = MusicPlayer(
            playBack=trackDB.getTrackList(),
            playlistList=playlistList,
            trackDB=trackDB
        )

        for play_list in self.media_player.playlistList:
            self.add_playlist_page(
                self.ui.Pages_Widget,
                play_list.getPlaylistName(),
                self.ui.listWidget_playlists,
                play_list.getTrackList()
            )

        self.clearAllComboBox()
        self.updateAllComboBox()

        with open(json_dir, encoding='utf-8') as f:
            data = json.load(f)

            if data['angry_playlist'] < 0:
                self.ui.comboBox_settings_emotion_playlist_map_angry.setCurrentText(
                    'None')
            else:
                self.media_player.angry_list = self.media_player.playlistList[
                    data['angry_playlist']]
                self.ui.comboBox_settings_emotion_playlist_map_angry.setCurrentText(
                    self.media_player.angry_list.getPlaylistName())

            if data['happy_playlist'] < 0:
                self.ui.comboBox_settings_emotion_playlist_map_happy.setCurrentText(
                    'None')
            else:
                self.media_player.happy_list = self.media_player.playlistList[
                    data['happy_playlist']]
                self.ui.comboBox_settings_emotion_playlist_map_happy.setCurrentText(
                    self.media_player.happy_list.getPlaylistName())

            if data['neutral_playlist'] < 0:
                self.ui.comboBox_settings_emotion_playlist_map_neutral.setCurrentText(
                    'None')
            else:
                self.media_player.neutral_list = self.media_player.playlistList[
                    data['neutral_playlist']]
                self.ui.comboBox_settings_emotion_playlist_map_neutral.setCurrentText(
                    self.media_player.neutral_list.getPlaylistName())

            if data['sad_playlist'] < 0:
                self.ui.comboBox_settings_emotion_playlist_map_sad.setCurrentText(
                    'None')
            else:
                self.media_player.sad_list = self.media_player.playlistList[data['sad_playlist']]
                self.ui.comboBox_settings_emotion_playlist_map_sad.setCurrentText(
                    self.media_player.sad_list.getPlaylistName())

            if data['surprise_playlist'] < 0:
                self.ui.comboBox_settings_emotion_playlist_map_surprise.setCurrentText(
                    'None')
            else:
                self.media_player.surprise_list = self.media_player.playlistList[
                    data['surprise_playlist']]
                self.ui.comboBox_settings_emotion_playlist_map_surprise.setCurrentText(
                    self.media_player.surprise_list.getPlaylistName())

        # PAGES
        ########################################################################

        # DASHBOARD PAGE
        self.ui.Btn_Dashboard.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_dashboard))

        # LIBRARY PAGE
        self.ui.Btn_Library.clicked.connect(self.on_library_open)

        # EMOTION RECOGNITION PAGE
        self.ui.Btn_menu_fer.clicked.connect(self.runLongTask)

        # SETTINGS PAGE
        self.ui.Btn_Settings.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings))
        self.ui.Btn_menu_settings.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings))

        # # SETTINGS: HAND GESTURE PAGE
        # self.ui.Btn_settings_hand_gesture.clicked.connect(
        #     lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_hand_gesture))
        # SETTINGS: EMOTION PLAYLIST MAP PAGE
        self.ui.Btn_settings_emotion_map.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_emotion_playlist_map))
        self.ui.btn_go_to_settings_no_playlist.clicked.connect(
            lambda: self.ui.Pages_Widget.setCurrentWidget(
                self.ui.page_settings_emotion_playlist_map)
        )
        # SETTINGS: BLUETOOTH PAGE
        self.ui.Btn_settings_bluetooth.clicked.connect(
            self.on_open_bluetooth_page)

        ## END PAGES ###########################################################

        # FUNCTIONALITY:
        ########################################################################
        ## Add song               ####
        self.ui.Btn_menu_add_songs.clicked.connect(
            lambda: self.on_add_songs_from_usb()
        )

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
            lambda: self.on_emotion_map_happy(self.ui.comboBox_settings_emotion_playlist_map_happy.currentIndex() - 1))
        self.ui.comboBox_settings_emotion_playlist_map_sad.activated[str].connect(
            lambda: self.on_emotion_map_sad(self.ui.comboBox_settings_emotion_playlist_map_sad.currentIndex() - 1))
        self.ui.comboBox_settings_emotion_playlist_map_angry.activated[str].connect(
            lambda: self.on_emotion_map_angry(self.ui.comboBox_settings_emotion_playlist_map_angry.currentIndex() - 1))
        self.ui.comboBox_settings_emotion_playlist_map_surprise.activated[str].connect(
            lambda: self.on_emotion_map_surprise(self.ui.comboBox_settings_emotion_playlist_map_surprise.currentIndex() - 1))
        self.ui.comboBox_settings_emotion_playlist_map_neutral.activated[str].connect(
            lambda: self.on_emotion_map_neutral(self.ui.comboBox_settings_emotion_playlist_map_neutral.currentIndex() - 1))
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
    # Scan USB
    def on_add_songs_from_usb(self):
        auto_detect_music_in_usb()
        updateTrackDatabaseFromFolderToJsonFile(
            # track_folder=os.path.join(
            # 'C:/', 'Users', 'Victus', 'Downloads', 'Music'),
            track_folder=os.path.join('/home/quangmnh/Music'),
            json_dir=json_dir
        )

        global trackDB, library_songs
        trackDB = getDBFromJSON(json_dir)
        library_songs = convert_from_track_list_to_list_dict(
            trackDB.getTrackList())
        self.media_player.trackDB = trackDB
        self.on_library_open()

    # Bluetooth
    def on_open_bluetooth_page(self):
        # Bluetooth settings page display change
        if (self.bluetooth.get_paired_device() != None):
            print("[DEBUG] current bluetooth device: ",
                  self.bluetooth.get_paired_device())
            self.ui.btn_settings_bluetooth_scan_devices.setText(
                "Device info: " + self.bluetooth.get_paired_device()["name"])
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(True)
        else:
            self.ui.btn_settings_bluetooth_scan_devices.setText("Scan devices")
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(False)
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_bluetooth)

    def on_scan_bluetooth_devices(self):
        # TODO: Scan bluetooth devices
        bluetooth_devices = None
        if self.bluetooth.get_paired_device() is None:
            bluetooth_devices = self.bluetooth.bluetooth_scan()
        # else:
        #     bluetooth_devices = self.bluetooth.get_paired_device()
        if bluetooth_devices is not None:
            display_list_item(self.ui.listWidget_settings_bluetooth_devices, [BluetoothDevice(
                device, on_connect_device=self.on_connect_device) for device in bluetooth_devices])

    def on_connect_device(self, device_info):
        # TODO: Connect to device
        self.bluetooth.connect_device(device_info["name"], device_info["mac"])
        if (self.bluetooth.get_paired_device() != None):
            print("[DEBUG] current bluetooth device: ",
                  self.bluetooth.get_paired_device())
            self.ui.btn_settings_bluetooth_scan_devices.setText(
                "Device info: " + self.bluetooth.get_paired_device()["name"])
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(True)
            self.ui.listWidget_settings_bluetooth_devices.clear()
        else:
            self.ui.btn_settings_bluetooth_scan_devices.setText("Scan devices")
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(False)
            self.ui.listWidget_settings_bluetooth_devices.clear()
        # self.on_scan_bluetooth_devices()

    def on_disconnect_device(self):
        device = self.bluetooth.get_paired_device()
        if device is None:
            return None
        else:
            disconnect_result = self.bluetooth.disconnect_device(device["mac"])
            if disconnect_result != None:
                if (self.bluetooth.get_paired_device() != None):
                    self.ui.btn_settings_bluetooth_scan_devices.setText(
                        "Device info: " + self.bluetooth.get_paired_device()["name"])
                    self.ui.btn_settings_bluetooth_scan_devices.setDisabled(
                        True)
                else:
                    self.ui.btn_settings_bluetooth_scan_devices.setText(
                        "Scan devices")
                    self.ui.btn_settings_bluetooth_scan_devices.setDisabled(
                        False)
            return 0
    # END: Bluetooth

    # Emotion Map
    def on_emotion_map_happy(self, playlistIndex: int):
        # TODO: Assign playlist to happy emotion according to user's input
        if playlistIndex < 0:
            updateEmotionPlaylistJson(json_dir, 'happy', -1)
            return
        self.media_player.happy_list = self.media_player.playlistList[playlistIndex]
        updateEmotionPlaylistJson(json_dir, 'happy', playlistIndex)

    def on_emotion_map_sad(self, playlistIndex: int):
        # TODO: Assign playlist to sad emotion according to user's input
        if playlistIndex < 0:
            updateEmotionPlaylistJson(json_dir, 'sad', -1)
            return
        self.media_player.sad_list = self.media_player.playlistList[playlistIndex]
        updateEmotionPlaylistJson(json_dir, 'sad', playlistIndex)

    def on_emotion_map_angry(self, playlistIndex: int):
        # TODO: Assign playlist to angry emotion according to user's input
        if playlistIndex < 0:
            updateEmotionPlaylistJson(json_dir, 'angry', -1)
            return
        self.media_player.angry_list = self.media_player.playlistList[playlistIndex]
        updateEmotionPlaylistJson(json_dir, 'angry', playlistIndex)

    def on_emotion_map_surprise(self, playlistIndex: int):
        # TODO: Assign playlist to surprise emotion according to user's input
        if playlistIndex < 0:
            updateEmotionPlaylistJson(json_dir, 'surprise', -1)
            return
        self.media_player.surprise_list = self.media_player.playlistList[playlistIndex]
        updateEmotionPlaylistJson(json_dir, 'surprise', playlistIndex)

    def on_emotion_map_neutral(self, playlistIndex: int):
        # TODO: Assign playlist to neutral emotion according to user's input
        if playlistIndex < 0:
            updateEmotionPlaylistJson(json_dir, 'neutral', -1)
            return
        self.media_player.neutral_list = self.media_player.playlistList[playlistIndex]
        updateEmotionPlaylistJson(json_dir, 'neutral', playlistIndex)
    # END : Emotion Map

    # Hand gesture
    def on_hand_gesture(self):
        # TODO: Enable and disable hand gesture script
        if self.ui.btn_settings_enable_hand_gesture.isChecked():
            print("Hand gesture enabled")
        else:
            print("Hand gesture disabled")
    # END: Hand gesture

    # Long running task
    def runLongTask(self):
        self.ui.Pages_Widget.setCurrentWidget(
            self.ui.page_emotion_recognition_loading)
        self.thread = QThread()
        self.worker = Worker(self.on_emotion_recognition, None)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(lambda: (self.thread.deleteLater(
        ), self.ui.Pages_Widget.setCurrentWidget(self.ui.page_emotion_recognition_no_playlist)))
        self.thread.start()

    # Emotion recognition
    def on_emotion_recognition(self):
        # TODO: PLease use the true label var for choosing and playing the right playlist
        temp = {
            "Angry": 0,
            "Happy": 0,
            "Neutral": 0,
            "Sad": 0,
            "Surprise": 0,
        }
        start = time()
        while time() - start < 4:
            frame = self.camera.get_frame()
            if frame is None:
                # print("frame is none")
                continue
            else:
                box = self.face_recognition.predict(
                    self.camera.get_blob(frame))
                if box is None:
                    continue
                else:
                    # print(box)
                    # print(frame.shape)
                    (height, width) = frame.shape[:2]
                    box = box * np.array([width, height, width, height])
                    # (x, y, w, h) = box.astype('int')
                    roi = self.camera.get_roi(box, frame)
                    if roi is None:
                        continue
                    else:
                        label = self.emotion_recognition.predict(roi)
                        temp[label] += 1
        true_label = max(temp, key=temp.get)
        # print(true_label)
        if true_label == 'Angry':
            self.media_player.curr_emotion_playlist = self.media_player.angry_list
        elif true_label == 'Happy':
            self.media_player.curr_emotion_playlist = self.media_player.happy_list
        elif true_label == 'Neutral':
            self.media_player.curr_emotion_playlist = self.media_player.neutral_list
        elif true_label == 'Sad':
            self.media_player.curr_emotion_playlist = self.media_player.sad_list
        else:
            self.media_player.curr_emotion_playlist = self.media_player.surprise_list

        if (self.media_player.curr_emotion_playlist.playListName == "" and self.media_player.curr_emotion_playlist.numOfTracks == 0):
            self.ui.label_fer_result_no_playlist.setText(
                "Currently there is no playlist mapped for " + true_label + " emotion. \n" + " Setup your preference now in Settings")
            self.ui.Pages_Widget.setCurrentWidget(
                self.ui.page_emotion_recognition_no_playlist)
            return
        self.media_player.playBack = self.media_player.curr_emotion_playlist.getTrackList()
        # self.change_playlist_page(
        #     self.ui.Pages_Widget,
        #     self.media_player.curr_emotion_playlist.getPlaylistName(),
        # )

        self.on_playlist_play(self.media_player.playBack)
        self.ui.label_fer_result.setText("Your current emotion is " + true_label +
                                         "\n Playing playlist " + self.media_player.curr_emotion_playlist.getPlaylistName())
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_emotion_recognition)

    # END: Emotion recognition

    # Library

    def on_library_open(self):
        # TODO: Display all the songs once the library is opened
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_library)
        display_list_item(
            self.ui.listWidget_library_songs,
            [LibrarySong(
                song,
                self.on_play_song,
                self.on_remove_song,
                self.add_to_playlist_dialog,
                # self.on_add_to_playlist,
                song.get('id'),
                self.media_player.trackDB.getTrackList()
            ) for song in library_songs]
        )

    def on_play_song(self, index: int, playback: "list[Track]" = []):
        self.media_player.playBack = playback
        self.media_player.playback_count = len(self.media_player.playBack)

        self.media_player.playSongAt(index)
        self.ui.change_label_player_track_in_navigator(
            self,
            trackName=self.media_player.playBack[index].getTrackName(),
            artistName=self.media_player.playBack[index].getArtistName()
        )

    def on_remove_song(self, index: int, _type: str = "", playlistName: str = ""):
        global library_songs

        if _type == "library_songs":
            if self.media_player.playBack != self.media_player.trackDB:
                self.media_player.playBack = self.media_player.trackDB

            trackDB.deleteTrackAtIndex(index)

            with open(json_dir, encoding='utf-8') as f:
                data = json.load(f)

                songdb = data.get('songdb')
                del songdb[index]

                idx = 0
                for song in songdb:
                    song['id'] = idx
                    idx += 1

            with open(json_dir, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            library_songs = convert_from_track_list_to_list_dict(
                self.media_player.getPlaybackList())

            display_list_item(
                self.ui.listWidget_library_songs,
                [LibrarySong(
                    song,
                    self.on_play_song,
                    self.on_remove_song,
                    self.add_to_playlist_dialog,
                    song.get('id'),
                    self.media_player.getPlaybackList()
                ) for song in library_songs]
            )

        else:
            # Assign to playlist
            self.media_player.deleteSong(index)

            new_playback = convert_from_track_list_to_list_dict(
                self.media_player.getPlaybackList()
            )

            with open(json_dir, encoding='utf-8') as f:
                data = json.load(f)

                play_list = data['play_list']
                for playlist in play_list:
                    if playlist['name'] == playlistName:
                        del playlist['songlist'][index]
                        playlist['count'] = playlist['count'] - 1

            with open(json_dir, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            self.change_playlist_page(
                self.ui.Pages_Widget,
                playlistName
                # new_playback,
                # self.media_player.getPlaybackList()
            )

    def add_to_playlist_dialog(self, trackIndex):
        print("Current trackIndex: ", trackIndex)
        Dialog = QtWidgets.QDialog(None)
        Dialog.setWindowTitle("Select playlist to add:")
        Dialog.resize(200, 100)
        buttonBox = QDialogButtonBox(Dialog)

        buttonBox.setGeometry(QtCore.QRect(15, 60, 170, 32))
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        comboBox = QtWidgets.QComboBox(Dialog)
        comboBox.setGeometry(QtCore.QRect(20, 20, 150, 22))
        for i, playlist in enumerate(self.media_player.playlistList):
            comboBox.addItem(playlist.getPlaylistName(), i)
        buttonBox.clicked.connect(Dialog.accept)
        buttonBox.rejected.connect(Dialog.reject)

        buttonBox.accepted.connect(lambda: self.on_add_to_playlist(
            playlistIndex=comboBox.currentData(), trackIndex=trackIndex))

        Dialog.exec_()
        # Get playlist index and add song to playlist

    def on_add_to_playlist(
            self,
            playlistIndex: int = 0,
            trackIndex: int = 0,
    ):
        # TODO: Add song to playlist
        with open(json_dir, encoding='utf-8') as f:
            data = json.load(f)

            playlist_info = data['play_list'][playlistIndex]
            song_list = playlist_info.get('songlist')
            if trackIndex in song_list:
                pass
            else:
                song_list.append(trackIndex)

            data['play_list'][playlistIndex]['songlist'] = song_list
            data['play_list'][playlistIndex]['count'] = len(song_list)

        with open(json_dir, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        new_trackDB = getDBFromJSON(json_dir)
        global trackDB
        trackDB = new_trackDB
        self.media_player = MusicPlayer(
            playBack=new_trackDB.getTrackList(),
            playlistList=getPlaylistList(json_dir, new_trackDB),
            trackDB=new_trackDB
        )

        playlistPage = self.media_player.playlistList[playlistIndex]
        self.change_playlist_page(
            self.ui.Pages_Widget,
            playlistPage.getPlaylistName()
        )

    # End : Library

    # Playlist
    def on_create_playlist(self):
        self.create_playlist_dialog(
            self.ui.Pages_Widget, self.ui.Pages_Widget, self.ui.listWidget_playlists)

    def on_playlist_song_play(self):
        # TODO : Play the song of the playlist
        # Đã implement, không cần xài hàm này nữa
        pass

    def on_playlist_play(self, trackList: "list[Track]" = []):
        # TODO : Play the playlist
        self.on_play_song(0, trackList)

    def create_playlist_dialog(self, parent: QtWidgets.QWidget, page_widget: QtWidgets.QStackedWidget, playlist_list_widget: QtWidgets.QListWidget):
        dialog = QtWidgets.QInputDialog(parent)
        dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        dialog.setWindowTitle("Create Playlist")
        dialog.setLabelText('Playlist Name:')
        dialog.setStyleSheet("color: white; background-color: rgb(50,50,50);")
        ok = dialog.exec_()
        playlist_name = dialog.textValue()

        if ok and playlist_name:
            # Check for duplicate playlist name
            for playlist in self.media_player.playlistList:
                if playlist.playListName == playlist_name:
                    msg = QMessageBox()
                    msg.setWindowTitle("Warning")
                    msg.setText(
                        "Playlist name already exists, please try again!")
                    msg.setIcon(QMessageBox.Information)

                    x = msg.exec_()

                    return

            self.add_playlist_page(
                page_widget,
                playlist_name,
                playlist_list_widget,
                trackList=[]
            )

            new_playlist = PlayList(
                name=playlist_name,
                trackList=[]
            )
            self.media_player.playlistList.append(new_playlist)

            with open(json_dir, encoding='utf-8') as f:
                data = json.load(f)

                play_list = data.get('play_list')

                new_data = {
                    "id": len(self.media_player.playlistList),
                    "name": playlist_name,
                    "count": 0,
                    "songlist": [],
                    "emotion_map": "None"
                }
                play_list.append(new_data)

                data['play_list'] = play_list

                self.clearAllComboBox()
                self.updateAllComboBox()

                if data['angry_playlist'] < 0:
                    self.ui.comboBox_settings_emotion_playlist_map_angry.setCurrentText(
                        'None')
                else:
                    self.media_player.angry_list = self.media_player.playlistList[
                        data['angry_playlist']]
                    self.ui.comboBox_settings_emotion_playlist_map_angry.setCurrentText(
                        self.media_player.angry_list.getPlaylistName())

                if data['happy_playlist'] < 0:
                    self.ui.comboBox_settings_emotion_playlist_map_happy.setCurrentText(
                        'None')
                else:
                    self.media_player.happy_list = self.media_player.playlistList[
                        data['happy_playlist']]
                    self.ui.comboBox_settings_emotion_playlist_map_happy.setCurrentText(
                        self.media_player.happy_list.getPlaylistName())

                if data['neutral_playlist'] < 0:
                    self.ui.comboBox_settings_emotion_playlist_map_neutral.setCurrentText(
                        'None')
                else:
                    self.media_player.neutral_list = self.media_player.playlistList[
                        data['neutral_playlist']]
                    self.ui.comboBox_settings_emotion_playlist_map_neutral.setCurrentText(
                        self.media_player.neutral_list.getPlaylistName())

                if data['sad_playlist'] < 0:
                    self.ui.comboBox_settings_emotion_playlist_map_sad.setCurrentText(
                        'None')
                else:
                    self.media_player.sad_list = self.media_player.playlistList[data['sad_playlist']]
                    self.ui.comboBox_settings_emotion_playlist_map_sad.setCurrentText(
                        self.media_player.sad_list.getPlaylistName())

                if data['surprise_playlist'] < 0:
                    self.ui.comboBox_settings_emotion_playlist_map_surprise.setCurrentText(
                        'None')
                else:
                    self.media_player.surprise_list = self.media_player.playlistList[
                        data['surprise_playlist']]
                    self.ui.comboBox_settings_emotion_playlist_map_surprise.setCurrentText(
                        self.media_player.surprise_list.getPlaylistName())

            with open(json_dir, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

    def add_playlist_page(
            self,
            page_widget: QtWidgets.QStackedWidget,
            playlist_name: str,
            playlist_list_widget: QtWidgets.QListWidget,
            trackList: "list[Track]",

    ):
        """Add playlist page to page stack widget

        Args:
            trackList (list[Track]): List contains track(s)
            page_widget (QtWidgets.QStackedWidget): Stack widget to add page to.
            playlist_name (str): Name of playlist to add.
            playlist_list_widget (QtWidgets.QListWidget): List widget to display all playlists.
        """
        playlist_label = PlaylistLabel(
            playlist_name,
            lambda: self.change_playlist_page(
                page_widget,
                playlist_name
            )
        )

        # Add label to list widget
        entry = QtWidgets.QListWidgetItem(playlist_list_widget)
        playlist_list_widget.addItem(entry)
        entry.setSizeHint(playlist_label.minimumSizeHint())
        playlist_list_widget.setItemWidget(entry, playlist_label)

        playlist_page = PlaylistPage(
            playlist_name,
            lambda: self.on_playlist_play(trackList),
            self.on_playlist_song_play,
            lambda: self.remove_playlist_page(
                page_widget, playlist_name, playlist_list_widget, entry),
            self.on_library_open,
        )
        # Add page to page stack
        page_widget.addWidget(playlist_page)

    def change_playlist_page(
            self,
            page_widget: QtWidgets.QStackedWidget,
            playlist_name: str
    ):
        # TODO: Display the playlist songs here also
        num_page = page_widget.count()
        for i in range(num_page):
            w = page_widget.widget(i)
            if hasattr(w, "playlist_name") and w.playlist_name == snake_case(playlist_name):
                page_widget.setCurrentIndex(i)

                with open(json_dir, encoding='utf-8') as f:
                    data = json.load(f)

                    play_list = data['play_list']
                    for playlist in play_list:
                        if playlist['name'] == playlist_name:
                            break

                    trackList = []

                    print(playlist['songlist'])
                    for idx in playlist['songlist']:
                        trackList.append(
                            self.media_player.trackDB.getTrackAtIndex(idx))

                track_list = convert_from_track_list_to_list_dict(trackList)

                display_list_item(
                    w.listWidget_playlist_songs,
                    [PlaylistSong(
                        song,
                        self.on_play_song,
                        self.on_remove_song,
                        song.get('id'),
                        trackList,
                        playlist_name
                    ) for song in track_list]
                )
                break

    def remove_playlist_page(
            self,
            page_widget: QtWidgets.QStackedWidget,
            playlist_name: str,
            playlist_list_widget: QtWidgets.QListWidget,
            playlist_label: QtWidgets.QListWidgetItem
    ):
        num_page = page_widget.count()
        for i in range(num_page):
            w = page_widget.widget(i)
            if hasattr(w, "playlist_name") and w.playlist_name == snake_case(playlist_name):
                page_widget.removeWidget(w)
                page_widget.setCurrentIndex(0)
                break

        # Delete playlist in playlistList of Music player
        self.media_player.deletePlaylist(playlist_name)

        # Remove label from list widget
        playlist_list_widget.takeItem(playlist_list_widget.row(playlist_label))

        flag = ""
        with open(json_dir, encoding='utf-8') as f:
            data = json.load(f)

            play_list = data['play_list']
            idx = 0
            for playlist in play_list:
                if playlist['name'] == playlist_name:
                    break
                idx += 1

            data['play_list'] = play_list

            if data['angry_playlist'] == playlist['id']:
                data['angry_playlist'] = -1
                self.media_player.angry_list = PlayList()
                flag = 'angry'
            elif data['happy_playlist'] == playlist['id']:
                data['happy_playlist'] = -1
                self.media_player.happy_list = PlayList()
                flag = 'happy'
            elif data['neutral_playlist'] == playlist['id']:
                data['neutral_playlist'] = -1
                self.media_player.neutral_list = PlayList()
                flag = 'neutral'
            elif data['sad_playlist'] == playlist['id']:
                data['sad_playlist'] = -1
                self.media_player.sad_list = PlayList()
                flag = 'sad'
            else:
                data['surprise_playlist'] = -1
                self.media_player.surprise_list = PlayList()
                flag = 'surprise'

            del play_list[idx]

        with open(json_dir, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.clearAllComboBox()
        self.updateAllComboBox()

        self.ui.comboBox_settings_emotion_playlist_map_angry.setCurrentText(
            self.media_player.angry_list.getPlaylistName()
        )
        self.ui.comboBox_settings_emotion_playlist_map_happy.setCurrentText(
            self.media_player.happy_list.getPlaylistName()
        )
        self.ui.comboBox_settings_emotion_playlist_map_neutral.setCurrentText(
            self.media_player.neutral_list.getPlaylistName()
        )
        self.ui.comboBox_settings_emotion_playlist_map_sad.setCurrentText(
            self.media_player.sad_list.getPlaylistName()
        )
        self.ui.comboBox_settings_emotion_playlist_map_surprise.setCurrentText(
            self.media_player.surprise_list.getPlaylistName()
        )

        if flag == 'angry':
            self.ui.comboBox_settings_emotion_playlist_map_angry.setCurrentText(
                'None')
        if flag == 'happy':
            self.ui.comboBox_settings_emotion_playlist_map_happy.setCurrentText(
                'None')
        if flag == 'neutral':
            self.ui.comboBox_settings_emotion_playlist_map_neutral.setCurrentText(
                'None')
        if flag == 'sad':
            self.ui.comboBox_settings_emotion_playlist_map_sad.setCurrentText(
                'None')
        if flag == 'surprise':
            self.ui.comboBox_settings_emotion_playlist_map_surprise.setCurrentText(
                'None')

    # End : Playlist

    # Player
    # Play/Pause buttong

    def on_mediastate_changed(self, state):
        if self.media_player.player.state() == QMediaPlayer.PlayingState:
            self.ui.btn_player_navigator_playPause.setIcon(
                self.pause_icon.icon)
        else:
            self.ui.btn_player_navigator_playPause.setIcon(self.play_icon.icon)

        if self.media_player.getCurrPos()/1000 >= self.media_player.playBack[self.media_player.curr_playing].getTrackDuration():
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

        if self.ui.btn_settings_enable_hand_gesture.isChecked():
            # Handle hand gesture
            # img = self.camera.get_frame()
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
        self.on_play_song(index, self.media_player.playBack)

    def on_previous_song(self):
        index = self.media_player.prev()
        self.on_play_song(index, self.media_player.playBack)

    def on_repeat_mode(self):
        self.media_player.changeRepeatMode()

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
    # End : Player

    # END : HANDLERS #######################################################

    def updateAllComboBox(self):
        self.ui.comboBox_settings_emotion_playlist_map_happy.addItem('None')
        self.ui.comboBox_settings_emotion_playlist_map_sad.addItem('None')
        self.ui.comboBox_settings_emotion_playlist_map_neutral.addItem('None')
        self.ui.comboBox_settings_emotion_playlist_map_surprise.addItem('None')
        self.ui.comboBox_settings_emotion_playlist_map_angry.addItem('None')

        for playlistPage in self.media_player.playlistList:
            self.ui.comboBox_settings_emotion_playlist_map_happy.addItem(
                playlistPage.getPlaylistName())
            self.ui.comboBox_settings_emotion_playlist_map_sad.addItem(
                playlistPage.getPlaylistName())
            self.ui.comboBox_settings_emotion_playlist_map_neutral.addItem(
                playlistPage.getPlaylistName())
            self.ui.comboBox_settings_emotion_playlist_map_surprise.addItem(
                playlistPage.getPlaylistName())
            self.ui.comboBox_settings_emotion_playlist_map_angry.addItem(
                playlistPage.getPlaylistName())

    def clearAllComboBox(self):
        self.ui.comboBox_settings_emotion_playlist_map_happy.clear()
        self.ui.comboBox_settings_emotion_playlist_map_sad.clear()
        self.ui.comboBox_settings_emotion_playlist_map_neutral.clear()
        self.ui.comboBox_settings_emotion_playlist_map_surprise.clear()
        self.ui.comboBox_settings_emotion_playlist_map_angry.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    json_dir = os.path.join('sample.json')

    trackDB = getDBFromJSON(json_dir)
    library_songs = convert_from_track_list_to_list_dict(
        trackDB.getTrackList())
    playlistList = getPlaylistList(json_dir, trackDB)

    window = MainWindow()
    sys.exit(app.exec_())
