import json
import os

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtCore import (QObject, QThread, pyqtSignal, QProcess)
from PyQt5 import QtCore, QtGui, QtWidgets
# GUI file
from utils1.snake_case import snake_case
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

# For testing initialize time
# from controller.model_manager import *
# END : For testing initialize time
from controller.blutooth_controller import *

# EXAMPLE DATA
############################################
playlist_no = 1

start_fer = 0

start_running = 0


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


class BluetoothWorker(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(str)

    def __init__(self, scan_method, connect_method, disconnect_method, parent: None) -> None:
        super().__init__(parent)
        self.scan_method = scan_method
        self.connect_method = connect_method
        self.disconnect_method = disconnect_method

    def run_scan(self):
        self.scan_method()
        self.finished.emit()

    def run_connect(self):
        self.connect_method()
        self.finished.emit()

    def run_disconnect(self):
        self.disconnect_method()
        self.finished.emit()


class TestProcess(QProcess):
    finish_initiate_signal = pyqtSignal(int)
    error_signal = pyqtSignal(int)
    emotion_result = pyqtSignal(str)

    def __init__(self, io_timeout=300):
        super().__init__()
        self.io_timeout = io_timeout

        self.finished.connect(
            lambda code, status: self._on_finished(code, status))

        self.readyReadStandardOutput.connect(
            lambda: self._on_output()
        )

        self.readyReadStandardError.connect(
            lambda: self._on_std_error()
        )

    def _on_finished(self, exit_code=None, exit_status=None):
        """
        """
        if not self.atEnd():
            std_out = self.readAllStandardOutput().data().decode().strip()
            std_err = self.readAllStandardError().data().decode().strip()

        # rest of function

    def _on_output(self):
        """
        """
        self.setReadChannel(QProcess.StandardOutput)

        # collect all data
        msg = b''
        # while self.waitForReadyRead(self.io_timeout):
        #     # new data waiting
        #     msg += self.readAllStandardOutput().data()
        msg += self.readAllStandardOutput().data()

        # rest of function
        # print("[DEBUG] Print from result received in process: ", msg.decode())
        if ("Angry" in msg.decode() or "Happy" in msg.decode() or "Neutral" in msg.decode() or "Sad" in msg.decode() or "Surprise" in msg.decode()):
            global start_fer
            print("[TEST] Emotion result time: ", time() - start_fer)
            self.emotion_result.emit(msg.decode())

    def _on_std_error(self):
        """
        """
        self.setReadChannel(QProcess.StandardError)

        # collect all data
        err = b''
        # new data waiting
        err += self.readAllStandardError().data()

        print("[DEBUG] Print from result received in process: ", err.decode())

        if ("WARN:0" in err.decode()):
            self.finish_initiate_signal.emit(1)
            return

        if ("timeout" in err.decode() or "TIMEOUT" in err.decode()):
            self.error_signal.emit(1)
            return


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # comment this section for windows testing and set these to None, fuk u all windows users
        # For testing initialize time
        # self.camera = CameraManagement()
        # self.face_recognition = ONNXClassifierWrapper2(
        #     "controller/new_caffe.trt", [1, 1, 200, 7], 0.5, target_dtype=np.float32)
        # self.emotion_recognition = ONNXClassifierWrapper(
        #     "controller/new_model.trt", [1, 5], target_dtype=np.float32)
        # END : For testing initialize time
        self.bluetooth = BluetoothController(5)

        # Start process for testing
        self.test_p = TestProcess(MainWindow)
        # For testing initialize time : Comment this
        self.test_p.start("python3", ["controller/fer.py"])
        # END : For testing initialize time

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

        # Set volume slider to 100
        self.ui.slider_player_volume.setValue(100)

        # PAGES
        ########################################################################

        # DASHBOARD PAGE
        self.ui.Btn_Dashboard.clicked.connect(self.on_dashboard_page)

        # LIBRARY PAGE
        self.ui.Btn_Library.clicked.connect(self.on_library_open)

        # EMOTION RECOGNITION PAGE
        # EXTRA
        self.ui.Btn_menu_fer.setDisabled(True)
        self.ui.Btn_menu_fer.setText("Currently loading...")
        self.test_p.emotion_result.connect(self.on_emotion_result)
        self.test_p.finish_initiate_signal.connect(
            lambda: (self.ui.Btn_menu_fer.setDisabled(False), self.ui.Btn_menu_fer.setText("Emotion recognition")))
        self.test_p.error_signal.connect(self.on_restart_process)
        # End : EXTRA

        # Fix the handler to on_emotion_recognition if failed
        self.ui.Btn_menu_fer.clicked.connect(
            lambda: (
                self.ui.Pages_Widget.setCurrentWidget(
                    self.ui.page_emotion_recognition_loading),
                self.test_p.write("Testing signal\n".encode()),
                self.assign_start_fer_time()
            )
        )

        # self.ui.Btn_menu_fer.clicked.connect(self.on_emotion_recognition)

        # SETTINGS PAGE
        self.ui.Btn_Settings.clicked.connect(self.on_setting_page)
        self.ui.Btn_menu_settings.clicked.connect(self.on_setting_page)

        # # SETTINGS: HAND GESTURE PAGE
        # self.ui.Btn_settings_hand_gesture.clicked.connect(
        #     lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_hand_gesture))
        # SETTINGS: EMOTION PLAYLIST MAP PAGE
        self.ui.Btn_settings_emotion_map.clicked.connect(
            self.on_emotion_playlist_map_page)
        self.ui.btn_go_to_settings_no_playlist.clicked.connect(
            self.on_emotion_playlist_map_page)
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
        # self.ui.btn_settings_bluetooth_scan_devices.clicked.connect(
        #     self.on_scan_bluetooth_devices)
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
        self.ui.slider_player_navigator_progress_bar.sliderMoved.connect(
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

    # EXTRA test
    def assign_start_fer_time(self):
        global start_fer
        start_fer = time()

    def on_emotion_result(self, result):
        true_label = result
        # print("[DEBUG] Print after signal: ", true_label)
        if ('Angry' in true_label or 'Happy' in true_label or 'Neutral' in true_label or 'Sad' in true_label or 'Surprise' in true_label):
            if 'Angry' in true_label:
                self.media_player.curr_emotion_playlist = self.media_player.angry_list
            elif 'Happy' in true_label:
                self.media_player.curr_emotion_playlist = self.media_player.happy_list
            elif 'Neutral' in true_label:
                self.media_player.curr_emotion_playlist = self.media_player.neutral_list
            elif 'Sad' in true_label:
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

            self.on_playlist_play(
                self.media_player.curr_emotion_playlist.getPlaylistName())
            self.ui.label_fer_result.setText("Your current emotion is " + true_label +
                                             "\n Playing playlist " + self.media_player.curr_emotion_playlist.getPlaylistName())
            self.ui.Pages_Widget.setCurrentWidget(
                self.ui.page_emotion_recognition)

    def on_restart_process(self):
        self.test_p.kill()
        self.ui.Btn_menu_fer.setDisabled(True)
        self.ui.Btn_menu_fer.setText("Currently restarting...")
        if (self.test_p.state() == QProcess.NotRunning):
            # print("[DEBUG] Restart on error")
            self.test_p.start("python3", ["controller/fer.py"])

    # End : EXTRA test

    # HANDLERS
    ########################################################################
    # Dashboard page
    def on_dashboard_page(self):
        start = time()
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_dashboard)
        print("[TEST] Dashboard page open time: ", time() - start)

    # Setting page
    def on_setting_page(self):
        start = time()
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings)
        print("[TEST] Setting page open time: ", time() - start)

    def on_emotion_playlist_map_page(self):
        start = time()
        self.ui.Pages_Widget.setCurrentWidget(
            self.ui.page_settings_emotion_playlist_map)
        print("[TEST] Emotion playlist map page open time: ", time() - start)

    # Scan USB
    def on_add_songs_from_usb(self):
        start = time()
        auto_detect_music_in_usb()
        updateTrackDatabaseFromFolderToJsonFile(
            # track_folder=os.path.join(
            # 'C:/', 'Users', 'Victus', 'Downloads', 'Music'),
            track_folder=os.path.join(
                # "C:/", "Users", "Victus", "Downloads", "Music"),
                "/home/quangmnh/Music"),
            # "D:/", "Music"),
            json_dir=json_dir
        )

        global trackDB, library_songs

        trackDB.trackList = []
        trackDB.numOfTracks = 0

        with open(json_dir, encoding='utf-8') as f:
            data = json.load(f)

            for song in data['songdb']:
                track = Track(
                    song.get('id'),
                    song.get('url')
                )
                trackDB.addTrack(track)
                # print(len(trackDB.getTrackList()))

        library_songs = convert_from_track_list_to_list_dict(
            trackDB.getTrackList())
        self.media_player.trackDB = trackDB
        print("[TEST] on add songs from usb time: ", time() - start)
        self.on_library_open()

    # Bluetooth

    def on_open_bluetooth_page(self):
        start = time()
        # Bluetooth settings page display change
        if (self.bluetooth.get_paired_device() != None):
            # print("[DEBUG] current bluetooth device: ",
            #   self.bluetooth.get_paired_device())
            self.ui.btn_settings_bluetooth_scan_devices.setText(
                "Device info: " + self.bluetooth.get_paired_device()["name"])
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(True)
        else:
            self.ui.btn_settings_bluetooth_scan_devices.setText("Scan devices")
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(False)
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_settings_bluetooth)
        print("[TEST] Bluetooth page open time: ", time() - start)

    def on_scan_bluetooth_devices(self):
        start = time()
        # TODO: Scan bluetooth devices
        bluetooth_devices = None
        if self.bluetooth.get_paired_device() is None:
            bluetooth_devices = self.bluetooth.bluetooth_scan()
        # else:
        #     bluetooth_devices = self.bluetooth.get_paired_device()
        if bluetooth_devices is not None:
            display_list_item(self.ui.listWidget_settings_bluetooth_devices, [BluetoothDevice(
                device, on_connect_device=self.on_connect_device) for device in bluetooth_devices])
        print("[TEST] Scan bluetooth devices time: ", time() - start)

    def on_connect_device(self, device_info):
        start = time()
        # TODO: Connect to device
        self.bluetooth.connect_device(device_info["name"], device_info["mac"])
        if (self.bluetooth.get_paired_device() != None):
            # print("[DEBUG] current bluetooth device: ",
            #   self.bluetooth.get_paired_device())
            self.ui.btn_settings_bluetooth_scan_devices.setText(
                "Device info: " + self.bluetooth.get_paired_device()["name"])
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(True)
            self.ui.listWidget_settings_bluetooth_devices.clear()
        else:
            self.ui.btn_settings_bluetooth_scan_devices.setText("Scan devices")
            self.ui.btn_settings_bluetooth_scan_devices.setDisabled(False)
            self.ui.listWidget_settings_bluetooth_devices.clear()
        # self.on_scan_bluetooth_devices()
        print("[TEST] Connect device time: ", time() - start)

    def on_disconnect_device(self):
        start = time()
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
            print("[TEST] Disconnect device time: ", time() - start)
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

    def print_result(self, n):
        print("[DEBUG] emotion fetched result: ", n)

    # Long running task bluetooth
    def run_long_scan(self):
        self.ui.btn_settings_bluetooth_scan_devices.setDisabled(True)
        self.ui.btn_settings_bluetooth_scan_devices.setText("Scanning...")
        self.thread = QThread()
        self.worker = BluetoothWorker(self.on_scan_bluetooth_devices, self.on_connect_device,
                                      self.on_disconnect_device, None)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_scan)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def run_long_connect(self, device_info):
        self.thread = QThread()
        self.worker = BluetoothWorker(self.on_scan_bluetooth_devices, self.on_connect_device,
                                      self.on_disconnect_device, None)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_connect)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def run_long_disconnect(self):
        self.thread = QThread()
        self.worker = BluetoothWorker(self.on_scan_bluetooth_devices, self.on_connect_device,
                                      self.on_disconnect_device, None)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_disconnect)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    # END: Long running task

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

        self.on_playlist_play(
            self.media_player.curr_emotion_playlist.getPlaylistName())
        self.ui.label_fer_result.setText("Your current emotion is " + true_label +
                                         "\n Playing playlist " + self.media_player.curr_emotion_playlist.getPlaylistName())
        self.ui.Pages_Widget.setCurrentWidget(self.ui.page_emotion_recognition)

    # END: Emotion recognition

    # Library

    def on_library_open(self):
        # TODO: Display all the songs once the library is opened
        start = time()
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
        print("[TEST] Library page open time: ", time() - start)

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
        start = time()
        global library_songs

        if _type == "library_songs":
            if self.media_player.playBack != self.media_player.trackDB:
                self.media_player.playBack = self.media_player.trackDB.getTrackList()

            trackDB.deleteTrackAtIndex(index)

            with open(json_dir, encoding='utf-8') as f:
                data = json.load(f)

                for play_list in data['play_list']:
                    songlist = play_list['songlist']
                    if index in songlist:
                        del songlist[songlist.index(index)]
                        play_list['count'] -= 1

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
            print("[TEST] Library song delete time: ", time() - start)

        else:
            # Assign to playlist
            curr_playlist = None
            for playlist in self.media_player.playlistList:
                if playlist.getPlaylistName() == playlistName:
                    curr_playlist = playlist
                    break

            if curr_playlist is not None:
                curr_playlist.deleteTrack(index)

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
            )
            print("[TEST] Playlist song delete time: ", time() - start)

    def add_to_playlist_dialog(self, trackIndex):
        # print("Current trackIndex: ", trackIndex)
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
        # print('Current playlist: ',
        #   self.media_player.playlistList[playlistIndex].getPlaylistName())
        start = time()
        with open(json_dir, encoding='utf-8') as f:
            data = json.load(f)

            playlist_info = data['play_list'][playlistIndex]
            song_list = playlist_info.get('songlist')
            if trackIndex in song_list:
                pass
            else:
                song_list.append(trackIndex)

            song_list.sort()
            data['play_list'][playlistIndex]['songlist'] = song_list
            data['play_list'][playlistIndex]['count'] = len(song_list)

        with open(json_dir, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.media_player.playlistList[playlistIndex].addTrack(
            self.media_player.trackDB.getTrackAtIndex(trackIndex)
        )

        playlistPage = self.media_player.playlistList[playlistIndex]
        self.change_playlist_page(
            self.ui.Pages_Widget,
            playlistPage.getPlaylistName()
        )
        print("[TEST] Add to playlist time: ", time() - start)
    # End : Library

    # Playlist
    def on_create_playlist(self):
        start = time()
        self.create_playlist_dialog(
            self.ui.Pages_Widget, self.ui.Pages_Widget, self.ui.listWidget_playlists)
        print("[TEST] Create playlist dialog time: ", time() - start)

    def on_playlist_song_play(self):
        # TODO : Play the song of the playlist
        # Đã implement, không cần xài hàm này nữa
        pass

    def on_playlist_play(self, playlist_name: str):
        # TODO : Play the playlist
        start = time()
        curr_playlist = None
        for playlist in self.media_player.playlistList:
            if playlist.getPlaylistName() == playlist_name:
                curr_playlist = playlist
                break

        if curr_playlist is not None:
            # print('[DEBUG]')
            # print(curr_playlist.printPlaylistInfo())
            if len(curr_playlist.getTrackList()) != 0:
                self.on_play_song(0, curr_playlist.getTrackList())
        print("[TEST] Play playlist time: ", time() - start)

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
                    "id": len(self.media_player.playlistList) - 1,
                    "name": playlist_name,
                    "count": 0,
                    "songlist": []
                }
                play_list.append(new_data)

                # data['play_list'] = play_list

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
            lambda: self.on_playlist_play(playlist_name),
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
        start = time()
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

                    # print(playlist['songlist'])
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
        print("[TEST] Change playlist page:", time() - start)

    def remove_playlist_page(
            self,
            page_widget: QtWidgets.QStackedWidget,
            playlist_name: str,
            playlist_list_widget: QtWidgets.QListWidget,
            playlist_label: QtWidgets.QListWidgetItem
    ):
        start = time()
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
        print("[TEST] Remove playlist page:", time() - start)

    # End : Playlist

    # Player
    # Play/Pause buttong

    def on_mediastate_changed(self, state):
        if self.media_player.player.state() == QMediaPlayer.PlayingState:
            self.ui.btn_player_navigator_playPause.setIcon(
                self.pause_icon.icon)
        else:
            self.ui.btn_player_navigator_playPause.setIcon(self.play_icon.icon)

        # print('LENGTH OF PLAYBACK: ', len(self.media_player.getPlaybackList()))
        if len(self.media_player.getPlaybackList()) > 0:
            if self.media_player.getCurrPos()/1000 >= self.media_player.playBack[self.media_player.curr_playing].getTrackDuration():
                global start_running
                print('[TEST] Elapsed time: ', time() - start_running)
                # Turn off repeat mode
                if self.media_player.repeatMode == 0:
                    if self.media_player.curr_playing == len(self.media_player.playBack) - 1:
                        pass
                    else:
                        self.on_next_song()
                # Repeat all tracks
                elif self.media_player.repeatMode == 1:
                    self.on_next_song()
                # Repeat only one track
                else:
                    self.on_play_song(
                        self.media_player.curr_playing, self.media_player.getPlaybackList())

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
        start = time()
        current_val = self.ui.slider_player_navigator_progress_bar.value()
        self.media_player.player.setPosition(current_val)
        print("[TEST] Set player position:", time() - start)

    def on_set_volume(self, volume):
        start = time()
        self.media_player.player.setVolume(volume)
        print("[TEST] Set player volume:", time() - start)

    # Navigator
    def on_play_pause(self):
        start = time()
        self.media_player.togglePlayPause()
        print("[TEST] Toggle play pause:", time() - start)

    def on_next_song(self):
        start = time()
        if self.media_player.repeatMode != 2:
            index = self.media_player.next()
            if index < len(self.media_player.playBack):
                self.on_play_song(index, self.media_player.playBack)
        print("[TEST] Next song:", time() - start)

    def on_previous_song(self):
        start = time()
        if self.media_player.repeatMode != 2:
            index = self.media_player.prev()
            if index < len(self.media_player.playBack):
                self.on_play_song(index, self.media_player.playBack)
        print("[TEST] Previous song:", time() - start)

    def on_repeat_mode(self):
        start = time()
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
        print("[TEST] Change repeat mode:", time() - start)

    def on_shuffle_mode(self):
        start = time()
        self.media_player.toggleShuffleMode()
        # Change icons
        if self.media_player.isShuffle:
            self.ui.btn_player_navigator_shuffle.setIcon(
                self.shuffle_enabled.icon)
        else:
            self.ui.btn_player_navigator_shuffle.setIcon(
                self.shuffle_icon.icon)
        print("[TEST] Change shuffle mode:", time() - start)
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
    os.environ["PYTHONUNBUFFERED"] = "1"
    start = time()
    app = QApplication(sys.argv)

    json_dir = os.path.join('sample.json')

    trackDB = getDBFromJSON(json_dir)
    library_songs = convert_from_track_list_to_list_dict(
        trackDB.getTrackList())
    playlistList = getPlaylistList(json_dir, trackDB)

    window = MainWindow()
    end = time()
    print(f"Initialize time: {end - start}")
    sys.exit(app.exec_())
