# import numpy as np
import os

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl
from copy import deepcopy
import random
import eyed3
import json


class Track:
    def __init__(
            self,
            trackId: int = 0,
            trackURL: str = "",
            imageURL: str = ""
    ) -> None:
        self.trackId = trackId
        self.trackURL = trackURL
        audio = eyed3.load(trackURL)
        self.name = audio.tag.title
        self.artist = audio.tag.artist
        self.duration = audio.info.time_secs
        self.imageURL = imageURL

    '''------------ DEFINE GETTER FUNCTIONS ----------'''

    def getTrackName(self) -> str:
        return self.name

    def getArtistName(self) -> str:
        return self.artist

    def getTrackDuration(self) -> int:
        return int(self.duration)

    def getTrackURL(self) -> str:
        return self.trackURL

    '''------------- DEFINE SETTER FUNCTIONS ----------'''

    def setImageURL(self, imageURL: str = "") -> None:
        self.imageURL = imageURL


class TrackDatabase:
    def __init__(
            self,
            trackList: "list[Track]" = []
    ) -> None:
        self.trackList = trackList
        self.numOfTracks = 0

    def addTrack(
            self,
            newTrack: Track
    ) -> None:
        self.trackList.append(newTrack)
        self.numOfTracks += 1

    def getTrackAtIndex(
            self,
            index: int = 0
    ) -> "any":
        if len(self.trackList) == 0:
            return None
        else:
            return self.trackList[index]

    def getTrackList(self) -> "list[Track]":
        return self.trackList

    def deleteTrackAtIndex(self, index: int) -> None:
        del self.trackList[index]

    def displayTrackDBInfo(self) -> None:
        for i in range(len(self.trackList)):
            print(
                f'Duration: {self.trackList[i].getTrackDuration()},\n'
                f'Artist: {self.trackList[i].getArtistName()},\n'
                f'Track name: {self.trackList[i].getTrackName()},\n'
                f'Track URL: {self.trackList[i].getTrackURL()},\n'
                f'-----------------------------------\n')


class PlayList:
    def __init__(
            self,
            trackList: "list[Track]" = [],
            name: str = "Unknown"
    ) -> None:
        self.playListName = name
        self.numOfTracks = len(trackList)
        self.trackList = trackList

    def addTrack(
            self,
            newTrack: Track
    ) -> None:
        self.trackList.append(newTrack)
        self.numOfTracks += 1

    def deleteTrack(self, index: int):
        del self.trackList[index]
        self.numOfTracks -= 1

    def getTrackAtIndex(
            self,
            index: int = 0
    ) -> "any":
        if len(self.trackList) == 0:
            return None
        else:
            return self.trackList[index]

    def getTrackList(self) -> "list[Track]":
        return self.trackList

    def getPlaylistName(self) -> str:
        return self.playListName

    def printPlaylistInfo(self) -> None:
        print(
            f'Playlist name: {self.playListName},\n'
            f'Number of Tracks: {self.numOfTracks},\n'
            f'-----------------------------------\n')

        for i in range(len(self.trackList)):
            print(
                f'Duration: {self.trackList[i].getTrackDuration()},\n'
                f'Artist: {self.trackList[i].getArtistName()},\n'
                f'Track name: {self.trackList[i].getTrackName()},\n'
                f'Track URL: {self.trackList[i].getTrackURL()},\n'
                f'-----------------------------------\n')


class MusicPlayer:
    def __init__(
            self,
            trackDB: TrackDatabase,
            playBack: "list[Track]" = [],
            playlistList: "list[PlayList]" = [],
            systemVolume: int = 0,
            isPlaying: bool = False,
            isShuffle: bool = False,
            repeatMode: int = 0,
            isMute: bool = False,
            currVolume: int = 0,
            name: str = "Unknown",
            artist: str = "Unknown",
            position: int = 0,
    ) -> None:
        self.systemVolume = systemVolume
        self.isPlaying = isPlaying
        self.isShuffle = isShuffle
        self.repeatMode = repeatMode
        self.isMute = isMute
        self.currVolume = currVolume
        self.name = name
        self.artist = artist
        self.position = position
        self.playBack = playBack
        self.playback_count = len(self.playBack)
        self.curr_playing = 0
        self.shuffle_pb = deepcopy(self.playBack)
        self.trackDB = trackDB

        # Mapping emotion playlist
        self.happy_list = PlayList()
        self.angry_list = PlayList()
        self.neutral_list = PlayList()
        self.sad_list = PlayList()
        self.surprise_list = PlayList()
        self.curr_emotion_playlist = PlayList()

        # List of playlists
        self.playlistList = playlistList

        # Media Player
        self.player = QMediaPlayer()

    def getPlaybackList(self) -> "list[Track]":
        return self.playBack

    def toggleShuffleMode(self) -> None:
        self.isShuffle = not self.isShuffle

    def addSong(self, track: Track):
        self.playBack.append(track)
        self.playback_count += 1

    def deleteSong(self, index):
        if self.playback_count > 0:
            del self.playBack[index]
            self.playback_count -= 1

    def deletePlaylist(self, playlist_name: str):
        idx = 0
        for playlist in self.playlistList:
            if playlist.getPlaylistName() == playlist_name:
                break
            idx += 1
        del self.playlistList[idx]

    def changeRepeatMode(self) -> None:
        self.repeatMode = (self.repeatMode + 1) % 3

    def playSongAt(self, index):
        print(self.playBack[index].getTrackURL())
        self.curr_playing = index
        media_content = QMediaContent(
            QUrl.fromLocalFile(self.playBack[index].getTrackURL()))
        self.player.setMedia(media_content)
        self.player.play()

    def toggleMuteMode(self) -> None:
        self.isMute = not self.isMute

    def togglePlayPause(self) -> None:
        if self.isCurrPlaying():
            self.player.pause()
        else:
            self.player.play()

    def setCurrVolume(self, currVolume: int) -> None:
        self.currVolume = currVolume
        # self.player.set_volume(currVolume)
        self.player.setVolume(currVolume)

    def getCurrPos(self):
        return self.player.position()

    def setCurrVolume(self, currVolume: int) -> None:
        # self.currVolume = currVolume
        # return self.player.get_volume(currVolume)
        return self.player.volume()

    def isCurrPlaying(self):
        return self.player.state() == QMediaPlayer.PlayingState

    def next(self):
        if self.isShuffle:
            self.curr_playing = random.randint(0, self.playback_count - 1)
        else:
            self.curr_playing = (self.curr_playing + 1) % self.playback_count
        return self.curr_playing

    def prev(self):
        if self.isShuffle:
            self.curr_playing = random.randint(0, self.playback_count - 1)
        else:
            if self.curr_playing > 0:
                self.curr_playing = (self.curr_playing - 1)
            else:
                self.curr_playing = self.playback_count - 1
        return self.curr_playing


def getDBFromJSON(json_dir: str) -> TrackDatabase:
    with open(json_dir, encoding='utf-8') as f:
        data = json.load(f)

        trackDB = TrackDatabase()
        for track_info in data['songdb']:
            track = Track(
                track_info.get("id"),
                track_info.get("url")
            )
            if track is not None:
                trackDB.addTrack(track)

    return trackDB


def getPlaylistList(
        json_dir: str,
        trackDB: TrackDatabase
) -> "list[PlayList]":

    playlistList = []

    with open(json_dir, encoding='utf-8') as f:
        data = json.load(f)

        for playlist_info in data['play_list']:

            id_list = playlist_info.get("songlist")
            trackList: "list[Track]" = []
            for idx in id_list:
                trackList.append(trackDB.getTrackAtIndex(idx))

            playlist = PlayList(
                trackList=trackList,
                name=playlist_info.get("name")
            )

            if playlist is not None:
                playlistList.append(playlist)

    return playlistList


if __name__ == '__main__':
    pass
